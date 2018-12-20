import pomdp
import random
import math
import numpy as np
from operator import itemgetter

class driver(pomdp.pomdp):
    def __init__(self, speed):
        # Speed is in m/s. Positions are in metres.
        self.speed = speed
        self.threshold = 0.875 # if abs(pos) is more than this, reward is negative
        self.max_pos = 2   # limit the state space, abs() should be larger than threshold

        # Action sets the driving wheel to this angle, in radians.
        # Note that this is clamped in self.update_car_pos() to at max
        # absolute value of 0.2 after possible action noise.
        self.n_actions = 10
        self.actions = np.linspace(-0.08,0.08, self.n_actions)
        if 0 not in self.actions:
            self.actions = np.append(self.actions, 0)
        
        # Noise is added to action from a normal distribution that has
        # mean = noise_bias and sd = noise.
        self.noise_bias = 0
        self.noise = 0

        # Action noise is dependent on action size and this
        # multiplier, and is added to actions to simulate noisy motor
        # movements of the driver.
        self.action_noise = 0

        # Probability of observing the correct position in the road.
        # Lower probabilities equate to, e.g., less visibility.
        self.obs_prob = 0.8

        # Populate a table of all possible discrete positions where.
        self.resolution = 4 # how many belief entries per metre
        self.possible_positions = np.linspace(-self.max_pos, self.max_pos, 2*self.max_pos*self.resolution+1)

        # The transition model stores the state-action->state->p
        # transition probabilities, with state as an index, and as
        # values a new table, that has action as an index and
        # state-probability tuples as values. These values are trained
        # with full observability before training the Q-table.
        self.transitions = []

        # How many discrete entropy or uncertainty values in the
        # Q-table ? Set this value by hand, and it is then calculated
        # as the number of values per one unit.
        self.n_uncertainties = 10

        # Max entropy or uncertainty. Min is 0
        b = 1/len(self.possible_positions)
        max_ent = b * math.log(b) * len(self.possible_positions)
        self.n_uncertainties = self.n_uncertainties / max_ent

        # Time span to refresh the car position and drive (seconds).
        # This needs to be fixed, otherwise the transition model will
        # not work. This refers to the cognitive see-think-act cycle
        # of the driver.
        self.refresh_time = 0.150

        super().__init__(0.1, 0.9, self.actions, epsilon = 0.1)

        # Internal clock.
        self.model_time = 0

        # Belief is a probability distribution over possible
        # positions. Start with uniform (initialised in self.clear()).
        # Here called pos_belief and not belief, because the super
        # already has self.belief, and we don't want to rewrite it.
        # The super's belief takes care of Q-table handling, but not
        # belief update. The super's belief is the augmented
        # (max,entropy) state, and this is the belief distribution
        # over possible discrete positions.
        self.pos_belief = {}

        # For output, log the current simulated model time, car x
        # position (0 = middle of the road), action (set steering
        # wheel to this amount of radians, negative is to the left and
        # positive to the right), steer (actual steering wheel
        # position after added noise), obtained reward, and whether
        # the model is looking at the road or not.
        self.data_header = "modeltime pos action steer reward attention"                

        self.clear()

    def clear(self):
        self.pos = 0       # 0 is the centre of the road
        self.iteration = 0
        self.model_time = 0
        super().clear()
        init_prob = 1./len(self.possible_positions)
        for p in self.possible_positions:
            self.pos_belief[p] = init_prob

    # Observe, act, learn, and get reward.
    def do_iteration(self, debug = False, has_attention = True):
        self.iteration += 1
        self.model_time += self.refresh_time
        self.update_belief(has_attention)
        # Get entropy / uncertainty, and discretisise it.
        uncertainty = round(self.uncertainty() * self.n_uncertainties) / self.n_uncertainties
        # Create the discretitised (max,entropy) belief state for storing in Q-table.
        belief = [max(self.pos_belief.items(), key=itemgetter(1))[0], uncertainty]
        self.set_belief_state(belief)

        if debug == True:
            print("Car belief:",self.belief)
            print("Car q:",self.q[self.belief])

        self.choose_action_epsilon()

        if self.learning: self.update_q_sarsa()
        # Update car position according to the action.
        if debug == True: print("Car pos",self.pos,"action",self.action)
        self.update_car_pos()
        self.calculate_reward()

        # Log data.
        self.add_data("{} {} {} {} {} {}".format(self.model_time, self.pos,
                                                 self.action, self.steer, self.reward, has_attention))

    # Learn the transitions by iterating all positions and simulating
    # the result of actions.
    def learn_transitions(self, iters, output_progress = False):
        # Init transition table.
        self.transitions = {}
        for pos in self.possible_positions:
            self.transitions[pos] = {}
            for a in self.actions:
                self.transitions[pos][a] = {}
                for pos2 in self.possible_positions:
                    self.transitions[pos][a][pos2] = 0

        # Iterate through all positions,action combinations and
        # observe the outcome multiple times.
        for a in self.actions:
            if output_progress: print("Creating transitions for", a)
            for pos in self.possible_positions:
                # Finer discrete positions within the represented belief.
                for pos_fine in np.linspace(-1/self.resolution+0.001,1/self.resolution-0.001,10):
                    for i in range(iters):
                        self.pos = pos + pos_fine
                        self.action = a
                        self.update_car_pos()
                        new_pos = round(self.pos*self.resolution) / self.resolution
                        self.transitions[pos][self.action][new_pos] += 1

        # Normalise transition table.
        for pos in self.possible_positions:
            for a in self.actions:
                if sum(self.transitions[pos][a].values()) > 0:
                    factor=1.0/sum(self.transitions[pos][a].values())
                    for pos2 in self.transitions[pos][a].keys():
                        self.transitions[pos][a][pos2] = self.transitions[pos][a][pos2]*factor

        self.clear()

    def update_car_pos(self):
        # Add noise to current action based on its size (signal-
        # dependent motor noise).
        self.steer = self.action + abs(self.action)*np.random.normal(0, self.action_noise)

        # Steer cannot exceed the maximum of 0.2 radians in any case.
        self.steer = max(-0.2,self.steer)
        self.steer = min(self.steer, 0.2)

        self.pos += self.speed * self.refresh_time * math.sin(self.steer)

        # Add noise to the position itself, dependent on the noise and speed.
        self.pos += np.random.normal(self.noise_bias, self.noise)*self.speed

        # Keep within the state space bounds.
        if self.pos > self.max_pos: self.pos = self.max_pos
        if self.pos < 0 and -self.pos > self.max_pos: self.pos = -self.max_pos
        return self.pos

    def calculate_reward(self):
        # If the car is over the threshold, give negative reward,
        # otherwise zero. To guide the car back to the road, the
        # penalty get larger with larger positions.
        if abs(self.pos) >= self.threshold:
            self.reward = -abs(self.pos)*2
        else:
            self.reward = 0

        return self.reward

    # Update the belief distribution of where the car is currently.
    # This depends on whether the driving model has attention or not.
    def update_belief(self, has_attention):
        # Use the model to predict positions.        
        if self.action != None:
            # Have to create a new dict, because adjacent positions
            # influence each other, so have to wait until all beliefs
            # are calculated before updating beliefs.
            tmp = {}

            for b in self.pos_belief.keys():
                total_prob = 0
                for pos1 in self.transitions:
                    total_prob += self.transitions[pos1][self.action][b] * self.pos_belief[pos1]
                tmp[b] = total_prob

            # Normalise and put back to pos_belief.
            s = sum(tmp.values(), 0.0)
            if s > 0: self.pos_belief = {k: v / s for k, v in tmp.items()}
            else: self.pos_belief = tmp

        # If the driver has attention, use the observation of the
        # current position to update belief.
        if self.action != None and has_attention == True:
            if random.random() < self.obs_prob:
                # True observation
                observed_pos = self.pos
            else:
                observed_pos = random.uniform(-self.max_pos, self.max_pos)
            
            for b in self.pos_belief.keys():
                # Bayes update. Increase the probability of the
                # current position, decrease others.
                if self.resolution*b == round(observed_pos*self.resolution):
                    # Note. Also trusting the model-based prior belief
                    # here, not just the observation.
                    self.pos_belief[b] = self.obs_prob*self.pos_belief[b]
                else:
                    # other positions
                    self.pos_belief[b] = (self.obs_prob/(len(self.pos_belief)-1))*self.pos_belief[b]

            # Normalise
            s = sum(self.pos_belief.values(), 0.0)
            if s > 0: self.pos_belief = {k: v / s for k, v in self.pos_belief.items()}


    # Driving model's uncertainty is the entropy of the belief distribution.
    def uncertainty(self):
        ent = 0
        for b in self.pos_belief.values():
            # sometimes the belief is so small it is rounded to 0
            if b > 0:
                ent += b * math.log(b)
        return -ent    

    # eyes_close is the probability of closing eyes, the duration, in
    # seconds is sampled from normal distribution with mean of
    # close_duration, and sd of half that.
    def run_model(self, max_time, eyes_close = 0, close_duration = 5, output_progress = False,
                  visualise = False):
        print_time = 0
        eyes_closed = 0
        sum_reward = 0
        sum_actions = 0
        while self.model_time < max_time:
            if output_progress and self.model_time >= print_time:

                print("Running model... ", round(self.model_time / max_time, 2),
                      len(self.q), round(sum_reward), round(sum_actions,3))
                print_time += max_time / 10
                sum_reward = 0
                sum_actions = 0

            # Close eyes?
            if eyes_closed <= 0 and eyes_close > 0 and random.random() < eyes_close:
                eyes_closed = np.random.normal(close_duration, close_duration / 2)
            if eyes_closed > 0:
                eyes_closed -= self.refresh_time
                eyes = False
            else:
                eyes = True
            self.do_iteration(debug = False, has_attention = eyes)
                
            if self.reward: sum_reward += self.reward
            if self.action: sum_actions += abs(self.action)

    def dump_q(self, filename):
        out = open(filename, "w")
        out.write("pos uncertainty action q\n")
        for s in self.q:
            s_split = s.split(",")
            s_pos = s_split[0].replace("[","").strip()
            s_ent = s_split[1].replace("]","").strip()
            for a in self.q[s]:
                out.write("{} {} {} {}".format(s_pos,s_ent,a,self.q[s][a]) + "\n")
        out.close()

# Subgoal 1. Investigate different driving speeds.
# Create the driver, driving at x m/s.
d = driver(33)
d.noise = 0.01
d.action_noise = 0
# Learn the transition table: given current belief distribution and an
# action, what is the new belief distribution.
d.learn_transitions(1000, output_progress = True)
d.log_data = True
# Use q-learning to learn.
d.run_model(100000, output_progress = True)
d.write_data_to_file("driver33.csv")

# Subgoal 2. First train, then simulate.
# d = discrete_driver(22)
# d.noise = 0.01
# d.action_noise = 0
# d.obs_prob = 0.3
# # Learn the transition table: given current belief distribution and an
# # action, what is the new belief distribution.
# d.learn_transitions(1000, output_progress = True)
# # Use q-learning to learn.
# d.run_model(100000, output_progress = True)
# # Run the model with no exploration (only exploit, i.e., drive as safely as possible).
# d.clear()
# d.log_data = True
# d.epsilon = 0
# d.run_model(10000, output_progress = True)
# d.write_data_to_file("driver22_o3.csv")

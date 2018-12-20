from operator import itemgetter # getting max q from a dict
import math
import random
import numpy as np

class pomdp():
    def __init__(self, alpha, gamma, actions, epsilon = 0.1, softmax_temp = 1.5):
        self.alpha = alpha
        self.gamma = gamma
        self.actions = actions

        self.epsilon = epsilon

        self.softmax_temp = softmax_temp

        self.q = {}

        self.context = ""

        self.data = []
        self.data_header = None
        self.log_data = False
        self.log_data_hooks = False
        self.log_hooks = []

        self.learning = True

        self.max_uncertainty = None


    # Clear the model, but not the q table. Note that init does not
    # clear the model, so clear() needs to be called before the first
    # task, as it takes care of task initialisation.
    def clear(self):
        self.action = None
        self.previous_action = None
        self.belief = None
        self.previous_belief = None

    # Logging

    def add_data(self, data):
        if self.log_data:
            self.data.append(data)
        if self.log_data_hooks:
            for lh in self.log_hooks:
                lh(self)

    def write_data_to_file(self, filename, clean = True):
        out = open(filename, "w")
        if self.data_header: out.write(self.data_header + "\n")
        for d in self.data:
            out.write(d + "\n")
        out.close()
        if clean:
            self.data = []

    # Reinforcement learning

    def calculate_max_q_value(self):
        return max(self.q[self.belief].items(), key=itemgetter(1))

    def current_q(self):
        return self.q[self.belief][self.action]

    # Get the smallest best action Q.
    def min_q(self):
        smallest = None
        for b in self.q:            
            candidate = max(self.q[b].items(), key=itemgetter(1))[1]
            if smallest and candidate < smallest:
                smallest = candidate
            elif not smallest:
                smallest = candidate
        return smallest

    def max_q(self):
        largest = None
        for b in self.q:
            for a in self.q[b]:
                if largest and self.q[b][a] > largest:
                    largest = self.q[b][a]
                elif not largest:
                    largest = self.q[b][a]
        return largest

    def update_q_learning(self, rounding = 10):
        if self.previous_action != None and self.learning:
            previous_q = self.q[self.previous_belief][self.previous_action]
            next_q = self.calculate_max_q_value()[1]
            self.q[self.previous_belief][self.previous_action] = \
                round(previous_q + self.alpha * (self.reward + self.gamma * next_q - previous_q), rounding)
            return self.q[self.previous_belief][self.previous_action]
        else:
            return None

    def update_q_sarsa(self, rounding = 10, debug = False):
        if self.previous_action != None and self.learning:
            previous_q = self.q[self.previous_belief][self.previous_action]
            if debug: print("Updating q for",self.previous_belief,self.previous_action, "reward =",self.reward)
            if debug: print("Previous q:", previous_q)
            next_q = self.q[self.belief][self.action]
            self.q[self.previous_belief][self.previous_action] = \
                previous_q + self.alpha * (self.reward + self.gamma * next_q - previous_q)
            if debug: print("New q     :", self.q[self.previous_belief][self.previous_action])
            return self.q[self.previous_belief][self.previous_action]
        else:
            return None

    def update_q_td(self, rounding = 10):
        if self.learning:
            previous_q = self.q[self.belief][self.action]
            self.q[self.belief][self.action] = \
                round(previous_q + self.alpha * (self.reward - previous_q), rounding)
            return self.q[self.belief][self.action]

    # Action selection

    def choose_action_epsilon(self):
        if self.action != None:
            self.previous_action = self.action            
        if random.random() < self.epsilon or sum(self.q[self.belief].values()) == 0:
            self.action = random.choice(self.actions)            
        else:
            self.action = self.calculate_max_q_value()[0]
        return self.action

    # Need this for softmax in case that actions are lists, because
    # numpy gets confused.
    def weighted_random(self, weights):
        number = random.random() * sum(weights.values())
        for k,v in weights.items():
            if number < v:
                break
            number -= v
        return k

    def choose_action_softmax(self):
        # Removed softmax.
        pass
    
    # For debugging.
    def softmax_values(self):
        pass
    
    # Belief management

    # Update belief to q if it does not exist, init with all actions = 0.0.
    def update_q(self, belief):
        if belief not in self.q:
            self.q[belief] = {}
            for action in self.actions:
                self.q[belief][action] = 0.0
        return self.q

    # Create a belief state from a list of states such that it is
    # hashable.
    def set_belief_state(self, states):
        if self.belief != None:
            self.previous_belief = self.belief
        self.belief = repr(states)
        self.update_q(self.belief)
        return self.belief

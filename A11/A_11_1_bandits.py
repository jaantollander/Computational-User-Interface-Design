import time
import random
from functools import partial
from random import uniform

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt


class BernoulliUniformBandit(object):
    def __init__(self, n, thetas, lows, highs):
        assert len(thetas) == len(lows) == len(highs) == n
        self.n = n
        self.thetas = thetas
        self.lows = lows
        self.highs = highs
        self.rewards = [t * (l + h) / 2 for (t, l, h) in
                        zip(thetas, lows, highs)]
        self.best_reward = max(self.rewards)

    def pull_arm(self, i):
        # Pull i-th arm and return reward
        if np.random.random() < self.thetas[i]:
            return uniform(self.lows[i], self.highs[i])
        else:
            return 0


class Solver(object):
    def __init__(self, bandit):
        """
        bandit (Bandit): the target bandit to solve
        """
        assert isinstance(bandit, BernoulliUniformBandit)
        np.random.seed(int(time.time()))

        self.bandit = bandit

        self.counts = [0] * self.bandit.n
        self.actions = []  # History of actions (list of arms pulled)
        self.regret = 0.  # Cumulative regret
        self.regrets = [0.]  # History of cumulative regrets

    def update_regret(self, i):
        # i: index of selected arm
        self.regret += self.bandit.best_reward - self.bandit.rewards[i]
        self.regrets.append(self.regret)

    @property
    def estimated_rewards(self):
        raise NotImplementedError

    def run_one_step(self):
        """Return the arm index to take action on."""
        raise NotImplementedError

    def run(self, num_steps):
        assert self.bandit is not None
        for _ in range(num_steps):
            i = self.run_one_step()

            self.counts[i] += 1
            self.actions.append(i)
            self.update_regret(i)


class EpsilonGreedy(Solver):
    def __init__(self, bandit, epsilon0, rate=0.0, init_reward=1.0):
        """
        epsilon (float): the probability to explore
        init_theta (float): We optimistically set initial theta to be 1.0

        Parameters
        ----------
        rate
        """
        super(EpsilonGreedy, self).__init__(bandit)
        assert 0. <= epsilon0 <= 1.0
        self.epsilon0 = epsilon0
        self.rate = rate
        # Optimisistic initialisation
        self.estimates = [init_reward] * self.bandit.n
        self.name = f"Epsilon-Greedy (epsilon={epsilon0}, rate={rate})"
        self.time = 0

    @property
    def estimated_rewards(self):
        return self.estimates

    def run_one_step(self):
        self.time += 1
        epsilon = self.epsilon0 / self.time ** self.rate
        if np.random.random() < epsilon:
            # We are going to explore
            i = np.random.randint(0, self.bandit.n)  # Pick a random arm
        else:
            # We are going to exploit
            i = max(range(self.bandit.n), key=lambda x: self.estimates[x])

        reward = self.bandit.pull_arm(i)  # Pull arm i and get reward
        # Update estimate for arm i
        self.estimates[i] += 1. / (self.counts[i] + 1) * \
                             (reward - self.estimates[i])
        return i


def run_solver(solver, trials=20, iterations=1000):
    regret_history = []
    for trial in range(trials):
        solver.regret = 0
        solver.regrets = []
        solver.run(iterations)
        regret_history.append(solver.regret)
    print(solver.name, np.mean(regret_history), "+/-", np.std(regret_history))


# TODO: 5 different bandits
thetas1 = [0.15, 0.30, 0.60]
lows1 = highs1 = [3, 2, 1]
bandit1 = BernoulliUniformBandit(len(thetas1), thetas1, lows1, highs1)

lows2 = [2, 1, 1]
highs2 = [2, 3, 2]
bandit2 = BernoulliUniformBandit(len(thetas1), thetas1, lows2, highs2)

# Select one of the bandit instances
bandit = bandit2

# Instantiate solvers
solvers = [
    EpsilonGreedy(bandit, 0.1, 0.0),
    EpsilonGreedy(bandit, 1.0, 0.8),
    EpsilonGreedy(bandit, 1.0, 1 / 2)
]

# Run experiment for each solver

for solver in solvers:
    num_trials = 20
    num_iterations = 1000
    run_solver(solver, num_trials, num_iterations)
    action_count = []
    for arm in range(bandit.n):
        action_count.append(solver.actions.count(arm) / num_trials)
    print("Actions per arm: ", action_count,
          "\n")  # Print number of times each arm was pulled

plt.figure()
for solver in solvers:
    plt.plot(solver.regrets, label=solver.name)

plt.legend()
plt.xlabel('time step')
plt.ylabel('cumulative regret')
plt.show()

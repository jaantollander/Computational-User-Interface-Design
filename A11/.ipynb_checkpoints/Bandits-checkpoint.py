{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# ELEC-E7851 Computational User Interface Design\n",
    "\n",
    "# Bandits (07.12.2018)\n",
    "### Kashyap Todi (www.kashyaptodi.com)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import time\n",
    "import random\n",
    "import numpy as np\n",
    "import scipy.stats\n",
    "import matplotlib.pyplot as plt"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Defining a Bandit\n",
    "\n",
    "We start by defining a Bandit.\n",
    "\n",
    "A bandit has $n$ arms.<br/>\n",
    "Each arm has a reward probability $\\theta$.<br/>\n",
    "When we pull an arm $i$, the bandit returns a reward with corresponding probability $i_\\theta$."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "class Bandit(object):\n",
    "    def __init__(self,n,thetas):\n",
    "        assert len(thetas) == n\n",
    "        self.n = n\n",
    "        self.thetas = thetas\n",
    "        self.best_theta = max(self.thetas)\n",
    "\n",
    "    def pull_arm(self, i):\n",
    "        # Pull i-th arm and return reward\n",
    "        if np.random.random() < self.thetas[i]:\n",
    "            return 1\n",
    "        else:\n",
    "            return 0\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's create two Bandit instances."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "thetas1 = [0.15,0.30,0.60]\n",
    "bandit1 = Bandit(len(thetas1),thetas1) #Define a 3-armed bandit\n",
    "\n",
    "thetas2 = [0.15,0.30,0.60,0.4,0.3,0.2,0.1,0.5,0.25]\n",
    "bandit2 = Bandit(len(thetas2),thetas2) #Define a 9-armed bandit"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Defining a Generic Solver\n",
    "\n",
    "A generic Bandit solver consists of:\n",
    "1. bandit: A Bandit object\n",
    "2. counts: Number of times each arm has been pulled\n",
    "3. actions: A History of actions taken (arms pulled)\n",
    "4. regret: Cumulative regret until current time step\n",
    "5. regrets: A history of cumulative regrets\n",
    "\n",
    "A solver must specify the steps taken during a single time step (`run_one_step`)\n",
    "\n",
    "A solver can be run $num\\ steps$ times, to calculate the cumulative regret and optionally the estimated $\\theta$s.\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "class Solver(object):\n",
    "    def __init__(self, bandit):\n",
    "        \"\"\"\n",
    "        bandit (Bandit): the target bandit to solve\n",
    "        \"\"\"\n",
    "        assert isinstance (bandit, Bandit)\n",
    "        np.random.seed(int(time.time()))\n",
    "        \n",
    "        self.bandit = bandit\n",
    "        \n",
    "        self.counts = [0] * self.bandit.n\n",
    "        self.actions = [] # History of actions (list of arms pulled)\n",
    "        self.regret = 0. # Cumulative regret\n",
    "        self.regrets = [0.] #History of cumulative regrets\n",
    "        \n",
    "    def update_regret(self, i):\n",
    "        # i: index of selected arm\n",
    "        self.regret += self.bandit.best_theta - self.bandit.thetas[i]\n",
    "        self.regrets.append(self.regret)\n",
    "        \n",
    "    @property\n",
    "    def estimated_thetas(self):\n",
    "        raise NotImplementedError\n",
    "        \n",
    "    def run_one_step(self):\n",
    "        \"\"\"Return the arm index to take action on.\"\"\"\n",
    "        raise NotImplementedError\n",
    "        \n",
    "    def run(self, num_steps):\n",
    "        assert self.bandit is not None\n",
    "        for _ in range(num_steps):\n",
    "            i = self.run_one_step()\n",
    "            \n",
    "            self.counts[i] += 1\n",
    "            self.actions.append(i)\n",
    "            self.update_regret(i)\n",
    "            \n",
    "        "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Defining an Experiment\n",
    "Let us now define an experiment to run the solver for n trials with m iterations each trial."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "def run_solver (solver, trials = 20, iterations = 1000):\n",
    "    regret_history = []\n",
    "    for trial in range(trials):\n",
    "        solver.regret = 0\n",
    "        solver.regrets = []\n",
    "        solver.run(iterations)\n",
    "        regret_history.append(solver.regret)\n",
    "    print(solver.name, np.mean(regret_history), \"+/-\",np.std(regret_history))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Implement Solvers\n",
    "\n",
    "### 1. Explore-Only:\n",
    "First, let's write a random solver, that randomly explores at every iteration:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "class Random(Solver):\n",
    "    def __init__(self, bandit):\n",
    "        super(Random, self).__init__(bandit)\n",
    "        self.name = \"Random\"\n",
    "            \n",
    "    def run_one_step(self):\n",
    "            i = np.random.randint(0, self.bandit.n) #Pick a random arm\n",
    "            reward = self.bandit.pull_arm(i) #Pull arm i and get reward\n",
    "            return i"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 2. Exploit-Only:\n",
    "Next, let's write a Greedy solver, that exploits a pre-determined arm at every iteration:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "class Greedy(Solver):\n",
    "    def __init__(self, bandit, arm):\n",
    "        super(Greedy, self).__init__(bandit)\n",
    "        self.arm = arm # Chosen arm (\"best-known\")\n",
    "        self.name = \"Greedy\"\n",
    "    \n",
    "    \n",
    "    def run_one_step(self):\n",
    "        reward = self.bandit.pull_arm(self.arm) #Pull arm i and get reward\n",
    "        return self.arm"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    " ### 3. $\\epsilon$-Greedy:\n",
    " \n",
    "We can explore random arms with a fixed probability ($\\epsilon$), while exploiting the best found arm otherwise.\n",
    " \n",
    "After each time step, we obtain reward r for pulling arm i.<br/>\n",
    "We update the estimated theta for arm i based on the outcome."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "class EpsilonGreedy(Solver):\n",
    "    def __init__(self, bandit, epsilon, init_theta=1.0):\n",
    "        \"\"\"\n",
    "        epsilon (float): the probability to explore\n",
    "        init_theta (float): We optimistically set initial theta to be 1.0\n",
    "        \"\"\"\n",
    "        super(EpsilonGreedy, self).__init__(bandit)\n",
    "        assert 0. <= epsilon <= 1.0\n",
    "        self.epsilon = epsilon\n",
    "        self.estimates = [init_theta]*self.bandit.n #Optimisistic initialisation\n",
    "        self.name = \"Epsilon-Greedy\"\n",
    "    @property\n",
    "    def estimated_thetas(self):\n",
    "        return self.estimates\n",
    "    \n",
    "    def run_one_step(self):\n",
    "        if np.random.random() < self.epsilon:\n",
    "            #We are going to explore\n",
    "            i = np.random.randint(0, self.bandit.n) #Pick a random arm\n",
    "        else:\n",
    "            #We are going to exploit\n",
    "            i = max(range(self.bandit.n), key=lambda x: self.estimates[x])\n",
    "\n",
    "        reward = self.bandit.pull_arm(i) #Pull arm i and get reward\n",
    "        self.estimates[i] += 1. / (self.counts[i]+1) * (reward - self.estimates[i]) #Update estimate for arm i\n",
    "        return i"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    " ### 4. UCB1:\n",
    " \n",
    "The Upper Confident Bound solver prefers arms with stronger potential for optimal value.\n",
    "\n",
    "At each step, we pick the best arm $i$ to maximise the upper confidence bound\n",
    "\n",
    "$a_t^{UCB}= argmax_{a\\in A} \\hat{Q_t}(a) + \\hat{U_t}(a)$<br><br>\n",
    "$\\hat{U_t}(a) = \\sqrt{\\dfrac{2 \\log t}{2N_t(a)}}$"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "class UCB1(Solver): #Upper-confidence bound\n",
    "    \n",
    "    def __init__(self, bandit, init_theta=1.0):\n",
    "        \"\"\"\n",
    "        init_theta (float): We optimistically set initial theta to be 1.0\n",
    "        \"\"\"\n",
    "        super(UCB1, self).__init__(bandit)\n",
    "        self.t = 0\n",
    "        self.estimates = [init_theta]*self.bandit.n #Optimisistic initialisation\n",
    "        self.name = \"UCB1\"\n",
    "        \n",
    "    @property\n",
    "    def estimated_thetas(self):\n",
    "        return self.estimates\n",
    "    \n",
    "    def run_one_step(self):\n",
    "        self.t += 1\n",
    "        \n",
    "        # Pick best one with consideration of upper confidence bounds\n",
    "        i = max(range(self.bandit.n), key=lambda\n",
    "                x: self.estimates[x] + np.sqrt(2*np.log(self.t)/(1+self.counts[x])))\n",
    "        reward = self.bandit.pull_arm(i)\n",
    "        \n",
    "        self.estimates[i] += 1. / (self.counts[i]+1) * (reward - self.estimates[i]) #Update estimate for arm i\n",
    "\n",
    "        return i"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    " ### 5. Thompson Sampling:\n",
    " \n",
    "The Thompson Sampling solver implements probability matching.\n",
    "\n",
    "For Bernoulli bandit, Q(a) follows a Beta distribution\n",
    "\n",
    "By default, $\\alpha$ and $\\beta$ are set to 1 (50% reward probability).<br>\n",
    "We can set initial $\\alpha$ and $\\beta$ based on our prior knowledge of reward probability.<br>\n",
    "\n",
    "After pulling an arm i, the $\\alpha$ and $\\beta$ for i is updated.\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "class ThompsonSampling(Solver):\n",
    "    def __init__(self, bandit, init_alpha=1, init_beta=1):\n",
    "        \"\"\"\n",
    "        init_a (int): initial value of a in Beta(a, b).\n",
    "        init_b (int): initial value of b in Beta(a, b).\n",
    "        \"\"\"\n",
    "        super(ThompsonSampling, self).__init__(bandit)\n",
    "\n",
    "        self._alphas = [init_alpha] * self.bandit.n\n",
    "        self._betas = [init_beta] * self.bandit.n\n",
    "        self.name = \"Thompson Sampling\"\n",
    "\n",
    "    @property\n",
    "    def estimated_probas(self):\n",
    "        return [self._alphas[i] / (self._alphas[i] + self._betas[i]) for i in range(self.bandit.n)]\n",
    "\n",
    "    def run_one_step(self):\n",
    "        samples = [np.random.beta(self._alphas[x], self._betas[x]) for x in range(self.bandit.n)]\n",
    "        i = max(range(self.bandit.n), key=lambda x: samples[x])\n",
    "        reward = self.bandit.pull_arm(i)\n",
    "\n",
    "        self._alphas[i] += reward\n",
    "        self._betas[i] += (1 - reward)\n",
    "\n",
    "        return i"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Test the solvers"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "We now test the solvers by running the experiment and printing the mean cumulative regret and standard deviation."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Random 248.175 +/- 6.776365176110286\n",
      "Actions per arm:  [328.4, 334.65, 336.95] \n",
      "\n",
      "Greedy 300.00000000000557 +/- 5.684341886080802e-14\n",
      "Actions per arm:  [0.0, 1000.0, 0.0] \n",
      "\n",
      "Epsilon-Greedy 30.832499999999982 +/- 28.35696243870271\n",
      "Actions per arm:  [32.75, 53.65, 913.6] \n",
      "\n",
      "UCB1 4.829999999999998 +/- 8.387347614114958\n",
      "Actions per arm:  [3.4, 11.0, 985.6] \n",
      "\n",
      "Thompson Sampling 0.7275 +/- 2.4794392007064823\n",
      "Actions per arm:  [1.15, 0.7, 998.15] \n",
      "\n"
     ]
    }
   ],
   "source": [
    "# Select one of the bandit instances\n",
    "bandit = bandit1\n",
    "\n",
    "# Instantiate solvers \n",
    "random = Random(bandit)\n",
    "greedy = Greedy(bandit,1)\n",
    "e_greedy = EpsilonGreedy(bandit,0.1) #Set epsilon = 0.1\n",
    "ucb1 = UCB1(bandit)\n",
    "thompson = ThompsonSampling(bandit)\n",
    "\n",
    "# Run experiment for each solver\n",
    "\n",
    "for solver in [random, greedy, e_greedy, ucb1, thompson]:\n",
    "    num_trials = 20\n",
    "    num_iterations = 1000\n",
    "    run_solver(solver,num_trials,num_iterations)\n",
    "    action_count = []\n",
    "    for arm in range(bandit.n):\n",
    "        action_count.append(solver.actions.count(arm)/num_trials)\n",
    "    print(\"Actions per arm: \",action_count, \"\\n\") #Print number of times each arm was pulled"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## In-class task 1: \n",
    "- Modify the bandit instance (add more arms, change $\\theta$s.\n",
    "- Change the target arm for Greedy.\n",
    "- Change $\\epsilon$ for $\\epsilon$-Greedy.\n",
    "- Specify strong prior for Thompson Sampling ( $\\alpha$ and $\\beta$ ).\n",
    "\n",
    "Observe and discuss how the results vary."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## In-class task 2:\n",
    "- For one trial, plot a comparative graph showing cumulative regrets over time for each solver.\n",
    "- Calculate *cumulative reward* over time for each solver, and construct the plot again.\n",
    "\n",
    "Discuss how they compare."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "for solver in [random, greedy, e_greedy, ucb1, thompson]:\n",
    "    plt.plot(solver.regrets, label = solver.name)\n",
    "\n",
    "\n",
    "plt.legend()\n",
    "plt.xlabel('time step')\n",
    "plt.ylabel('cumulative regret')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [default]",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

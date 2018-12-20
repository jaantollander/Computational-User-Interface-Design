from functools import partial

import matplotlib.pyplot as plt
import numpy as np
from GPyOpt.methods import BayesianOptimization


def f(x):
    return (2*x-2)**2 * np.cos(5*x-4)**2 + 2*x**2


def f_noisy(x, s=0.1):
    return f(x) + s * np.random.randn()


domain = [{'name': 'x', 'type': 'continuous', 'domain': (-1, 1)}]
opt = BayesianOptimization(f, domain=domain, exact_feval=True)
opt.run_optimization(max_iter=15)
opt.plot_acquisition()
# for _ in range(15):
#     opt.run_optimization(max_iter=1)
#     opt.plot_acquisition()


domain = [{'name': 'x', 'type': 'continuous', 'domain': (-1, 1)}]
opt = BayesianOptimization(partial(f_noisy, s=1.0), domain=domain, exact_feval=False)
opt.run_optimization(max_iter=15)
opt.plot_acquisition()


plt.figure()
x = np.linspace(-1, 1, 1000)
plt.plot(x, f(x))
plt.show()

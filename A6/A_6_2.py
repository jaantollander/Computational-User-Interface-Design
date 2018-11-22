import numpy as np
from GPyOpt.methods import BayesianOptimization
import matplotlib.pyplot as plt


def f(x):
    """The function to optimize.

    Parameters
    ----------
    x : np.ndarray
        1 dimensional array of 3 item representing the values `(r,g,b)` of rgb
        color.

    Returns
    -------
        int:
        The user given grade for the color `x`.
    """
    print(x)
    im = x.reshape(1, 1, 3).repeat(3, axis=0).repeat(3, axis=1)
    plt.figure(1)
    plt.imshow(im)
    plt.show(block=False)
    while True:
        res = input('Grade? (0 to 5) ')
        if res in ['0', '1', '2', '3', '4', '5']:
            res = int(res)
            plt.close(1)
            return res


def g(x):
    return f(np.array([x, x, x]))


domain = [{'name': 'color',
           'type': 'discrete',
           'domain': list(range(0, 255))}]
opt = BayesianOptimization(g, domain=domain, exact_feval=True, maximize=True)
opt.run_optimization(max_iter=2)
opt.plot_acquisition()
print(opt.x_opt, opt.fx_opt)

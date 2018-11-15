import math

import numpy as np
import pandas
import matplotlib.pyplot as plt


def low_pass_filter(a, x, x_prev):
    return a * x + (1 - a) * x_prev


def alpha(te, cutoff):
    tau = 1.0 / (2 * math.pi * cutoff)
    return 1.0 / (1.0 + tau / te)


class OneEuroFilter:
    def __init__(self, t0, x0, dx0=0.0, min_cutoff=1.0, beta=0.0, d_cutoff=1.0):
        self.min_cutoff = float(min_cutoff)
        self.beta = float(beta)
        self.d_cutoff = float(d_cutoff)

        self.x_prev = float(x0)
        self.dx_prev = float(dx0)
        self.t0 = float(t0)

    def __call__(self, t, x):
        t_e = t - self.t0

        # Derivative of the signal
        ad = alpha(t_e, self.d_cutoff)
        dx = (x - self.x_prev) / t_e
        dx_hat = low_pass_filter(ad, dx, self.dx_prev)

        # Value of the signal
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = alpha(t_e, cutoff)
        x_hat = low_pass_filter(a, x, self.x_prev)

        # Memorize the values.
        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.t0 = t

        return x_hat


if __name__ == '__main__':
    df = pandas.read_csv("A_5_1_noise.csv")
    t, x = df.values[:, 0], df.values[:, 1]

    # Try different paramaters
    for min_cutoff in [1.0, 0.5, 0.1, 0.01, 0.005, 0.001]:
        for beta in [0.1, 0.01, 0.007, 0.005, 0.003, 1e-3]:
            one_euro_filter = OneEuroFilter(
                t[0], x[0],
                min_cutoff=min_cutoff, beta=beta)
            x2 = np.zeros_like(x)
            x2[0] = x[0]
            for i in range(1, len(t)):
                x2[i] = one_euro_filter(t[i], x[i])

            plt.plot(t, x, alpha=0.3, color="cyan")
            plt.plot(t, x2, color="blue")
            plt.plot(t, np.abs(x-x2), color="red", alpha=0.5)
            plt.title(f"min_cutoff: {min_cutoff}, beta: {beta}")
            plt.show()

import math
from os import makedirs

import matplotlib.pyplot as plt
import numpy as np
import pandas
from matplotlib.animation import MovieWriter
from matplotlib.cbook import mkdirs


def low_pass_filter(a, x, x_prev):
    return a * x + (1 - a) * x_prev


def smoothing_factor(te, cutoff):
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
        a_d = smoothing_factor(t_e, self.d_cutoff)
        dx = (x - self.x_prev) / t_e
        dx_hat = low_pass_filter(a_d, dx, self.dx_prev)

        # Value of the signal
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = smoothing_factor(t_e, cutoff)
        x_hat = low_pass_filter(a, x, self.x_prev)

        # Memorize the values.
        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.t0 = t

        return x_hat


def plots():
    df = pandas.read_csv("A_5_1_noise.csv")
    t, x = df.values[:, 0], df.values[:, 1]

    # Try different paramaters
    directory = "A_5_1_figures"
    makedirs(directory, exist_ok=True)
    for min_cutoff in np.linspace(0.01, 0.005, 6):
        for beta in np.linspace(0.01, 0.001, 10):
            print("plotting:", min_cutoff, beta)
            one_euro_filter = OneEuroFilter(
                t[0], x[0],
                min_cutoff=min_cutoff, beta=beta)
            x2 = np.zeros_like(x)
            x2[0] = x[0]
            for i in range(1, len(t)):
                x2[i] = one_euro_filter(t[i], x[i])

            plt.figure()
            plt.plot(t, x, alpha=0.4, color="cyan")
            plt.plot(t, x2, color="blue")
            # plt.plot(t, np.abs(x-x2), color="red", alpha=0.3)
            plt.title(f"min_cutoff: {min_cutoff:.3f}, beta: {beta:.3f}")
            # plt.show()
            plt.savefig(f"{directory}/{min_cutoff:.3f}_{beta:.3f}.png", dpi=300)


def plot_signal():
    import seaborn
    seaborn.set()
    df = pandas.read_csv("A_5_1_noise.csv")
    t, x = df.values[:, 0], df.values[:, 1]

    plt.figure()
    plt.plot(t, x)
    plt.xlabel("$t$")
    plt.ylabel("$X$")
    plt.savefig("figures/noise.png", dpi=300)


def plot_filtered_signal(min_cutoff=0.008, beta=0.002):
    import seaborn
    seaborn.set()
    df = pandas.read_csv("A_5_1_noise.csv")
    t, x = df.values[:, 0], df.values[:, 1]

    one_euro_filter = OneEuroFilter(
        t[0], x[0],
        min_cutoff=min_cutoff, beta=beta)
    x2 = np.zeros_like(x)
    x2[0] = x[0]
    for i in range(1, len(t)):
        x2[i] = one_euro_filter(t[i], x[i])

    plt.figure()
    plt.plot(t, x, alpha=0.4, color="cyan")
    plt.plot(t, x2, color="blue")
    plt.title(f"min_cutoff: {min_cutoff:.3f}, beta: {beta:.3f}")

    plt.xlabel("$t$")
    plt.ylabel("$X$")
    plt.savefig(f"figures/noise_filtered_{min_cutoff:.3f}_{beta:.3f}.png", dpi=300)


if __name__ == '__main__':
    # plot_signal()
    # plot_filtered_signal()
    plots()

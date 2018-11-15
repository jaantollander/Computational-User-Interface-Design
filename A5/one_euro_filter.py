import math


def low_pass_filter(a, x, x_prev):
    return a * x + (1 - a) * x_prev


def alpha(te, cutoff):
    tau = 1.0 / (2 * math.pi * cutoff)
    return 1.0 / (1.0 + tau / te)


class OneEuroFilter:
    def __init__(self, min_cutoff=1.0, beta=0.0, dcutoff=1.0):
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.dcutoff = dcutoff

        # TODO: initial values as arguments?
        self.x = None   # Value
        self.dx = None  # Derivative of the value
        self.x_prev = None
        self.dx_prev = None
        self.t0 = None

    def __call__(self, x, t1):
        t_e = t1 - self.t0

        # Derivative
        ad = alpha(t_e, self.dcutoff)
        dx = (x - self.x_prev) / t_e
        dx_hat = low_pass_filter(ad, dx, self.dx_prev)

        # Filtered value
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = alpha(t_e, cutoff)
        x_hat = low_pass_filter(a, x, self.x_prev)

        # Memorize the values.
        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.t0 = t1

        return x_hat

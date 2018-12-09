import numpy as np
import seaborn
from scipy.optimize import newton
import matplotlib.pyplot as plt

a = 2.76
b = -2.83


def g(t):
    return a*np.log(t)+b


seaborn.set()
plt.figure()
plt.title(f"$a={a}$ and $b={b}$")
t = np.linspace(1, 50)
plt.plot(t, g(t), label=f'$g(t_w)$')
t_Bs = [0.1, 0.5, 1, 5, 10, 20, 30, 40, 50, 60]
t_w_opts = []

for t_B in t_Bs:
    x0 = 10
    t_w_opt = newton(
        lambda t_w: a * t_w * np.log(t_w) + b*t_w - a * t_w - a * t_B,
        x0, maxiter=100)
    t_w_opts.append(t_w_opt)
    plt.plot(t_w_opt, g(t_w_opt), 'o',
             label=f'$t_w={t_w_opt:.2f}$, $t_B={t_B:.2f}$')

plt.xlabel(r"$t_w$")
plt.ylabel(r"$g(t_w)$")
plt.legend()
plt.show()
# plt.savefig("figures/foraging_time.png", dpi=300)

plt.figure()
plt.title(f"$a={a}$ and $b={b}$")
plt.plot(t_Bs, t_w_opts, '-o')
plt.xlabel("$t_B$")
plt.ylabel("Optimal $t_w$")
plt.show()
# plt.savefig("figures/foraging_time2.png", dpi=300)

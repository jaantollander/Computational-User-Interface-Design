from os import makedirs

import matplotlib.pyplot as plt
import numpy as np
import seaborn


makedirs("figures", exist_ok=True)


seaborn.set()
plt.figure()
s = np.arange(15, 101)
e = 1236.5/(s-15)**0.618-72.5
plt.plot(s, e)
plt.xlabel("Strength (% max)")
plt.ylabel("Endurance Time (seconds)")
plt.xticks(np.arange(15, 100+5, 5))
plt.savefig("figures/strength-endurance.png", dpi=300)
# plt.show()


seaborn.set()
plt.figure()
m = np.linspace(0, 1, 101)
r_m = 15/100 * (22.94/((2.1+1.2+0.4+m)*9.81))
r_f = 15/100 * (18.57/((1.7+1.0+0.4+m)*9.81))
plt.plot(m, r_m, label="Males")
plt.plot(m, r_f, label="Females")
plt.xlabel("$m_w$")
plt.ylabel("$r_x$")
plt.xticks(m[::10])
plt.legend()
plt.savefig("figures/loaded-hand.png", dpi=300)
# plt.show()

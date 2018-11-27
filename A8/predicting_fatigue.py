import matplotlib.pyplot as plt
import numpy as np
import seaborn


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

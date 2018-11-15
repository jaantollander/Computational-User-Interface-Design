import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.stats.mstats_basic import linregress

# Fine-grain measurement data (step = 0.1 mm)
disp_fine = np.arange(0.0, 4.1, 0.1)
key_fine = np.array([
    2325, 2307, 2297, 2290, 2283, 2273, 2266, 2258, 2247, 2231, 2232,
    2220, 2210, 2197, 2170, 2157, 2149, 2133, 2112, 2094, 2081, 2054,
    2031, 2007, 1982, 1953, 1921, 1884, 1852, 1817, 1779, 1739, 1707,
    1647, 1592, 1531, 1461, 1383, 1305, 1219, 1129])

# Coarse-grain measurement data (step = 1.0 mm)
disp_coarse = np.arange(0.0, 4.5, 1.0)
key_coarse = np.array([2325, 2232, 2081, 1779, 1129])

# Calibration models
calibrate = interp1d(disp_coarse, key_coarse)
slope, intercept, rvalue, pvalue, stderr = linregress(disp_coarse, key_coarse)

# The figures
# import seaborn; seaborn.set()  # Prettier plots
plt.grid()
plt.plot(disp_fine, key_fine, "-", label="Fine")
plt.plot(disp_coarse, key_coarse, "X", label="Coarse")
plt.plot([disp_coarse[0], disp_coarse[-1]],
         [key_coarse[0], key_coarse[-1]], "--", label="Start-End")
plt.plot(disp_fine, calibrate(disp_fine), label="interp1d")
plt.plot(disp_fine, intercept + slope * disp_fine,
         label=f"linregress:\n{intercept}+({slope})x")
plt.xlabel('Key displacement in mm')
plt.ylabel('raw sensor value')
plt.legend()
# plt.savefig("figures/calibration.png", dpi=300)
plt.show()

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("A_5_1_noise.csv")
plt.plot(df.values[:, 0], df.values[:, 1])
plt.show()

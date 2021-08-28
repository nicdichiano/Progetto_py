import numpy as np
from matplotlib import pyplot as plt

rng = np.random.default_rng(42)
x = np.arange(1, 6)
y = rng.integers(low=0, high=30, size=5)
fig, ax = plt.subplots()
ax.plot(x, y)
print(x,y)
print(rng)
plt.show()
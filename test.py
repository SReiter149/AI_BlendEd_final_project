from numpy import tanh
import numpy as np
from matplotlib import pyplot as plt

x = np.array(list(range(-300,300)))
x = x/100
y = tanh(x)

print(x)
print(y)

print(tanh(0))

plt.plot(x,y)
plt.show()
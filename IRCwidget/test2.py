import numpy as np
import matplotlib.pyplot as plt

# Generar un array de valores de tiempo
t = np.linspace(start=0, num=96000*5, stop=5)

a = np.sin(2*np.pi*(9.9**t)*t)

plt.plot(t, a)
plt.show()

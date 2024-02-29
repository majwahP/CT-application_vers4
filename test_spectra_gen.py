import spekpy as sp
import matplotlib.pyplot as plt

s = sp.Spek(kvp=100,th=12)
s.filter('Al',6)
k, phi = s.get_spectrum(edges=True)

plt.plot(k, phi)
plt.show()
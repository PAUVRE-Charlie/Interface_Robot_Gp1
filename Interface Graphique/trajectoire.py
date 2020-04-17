import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

t = np.arange(0, 1.1, .1)
x = np.array([0,1,1,-1,-1])
y = np.array([0,1,-1,-1,1])
tck, u = interpolate.splprep([x, y], s=0)
unew = np.arange(0, 1.01, 0.01)
out = interpolate.splev(unew, tck)
plt.figure()
plt.plot(x, y, 'x', out[0], out[1])
plt.legend(['Linear', 'Cubic Spline', 'True'])
plt.axis([-1.05, 1.05, -1.05, 1.05])
plt.title('Spline of parametrically-defined curve')
plt.show()

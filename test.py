import numpy
import bohrium as np
print(np.bh_info.runtime_info())

def heat2d(height, width, epsilon=42):
  G = np.zeros((height+2,width+2),dtype=np.float64)
  G[:,0] = -273.15
  G[:,-1] = -273.15
  G[-1,:] = -273.15
  G[0,:] = 40.0
  center = G[1:-1,1:-1]
  north = G[:-2,1:-1]
  south = G[2:,1:-1]
  east = G[1:-1,:-2]
  west = G[1:-1,2:]
  delta = epsilon+1
  while delta > epsilon:
    tmp = 0.2*(center+north+south+east+west)
    delta = np.sum(np.abs(tmp-center))
    center[:] = tmp
  return center

res = heat2d(100, 100)
import sys
print(sys.executable)

from matplotlib import pyplot as plt
res = heat2d(100, 100)
plt.matshow(res, cmap='hot')
plt.show()
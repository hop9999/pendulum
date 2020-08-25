import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('data_static.csv',delimiter = ',')

time = data[200:,0]
x = data[200:,1]
vel = data[200:,2]
cur = data[200:,3]

m = 0.126
g = 9.8
l = 0.15
X = np.array([m*g*l*np.sin(x)])
U = np.array([cur])
print(X,U)
km = np.dot(X,np.linalg.pinv(U))
print(km)

plt.plot(time,x,label="x")
plt.legend()
plt.show()
plt.plot(time,cur,label="cur")
plt.plot(time,m*g*l*np.sin(x)/km[0][0],label="cur_calc")
plt.legend()
plt.show()
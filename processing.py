import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('data_dyn.csv',delimiter = ',')

time = data[:,0]
time_prev = -3e-4
pos = data[:,1]
vel = data[:,2]
cur = data[:,3]

km = 0.03
mgl = 0.183#self.m*self.g*self.l
I = 0.0040#self.I
k_x = 0.001

A = np.array([[0, 1],
              [-mgl*np.cos(0)/I, -k_x/I]])

B = np.array([[0],
              [km/I]])
e = 0.1
L = np.array([[0.1/e],
              [0.1/e**2]])

x = np.array([[1],
              [1]])

G = np.array([[0],
              [0]])

x_ar = np.zeros((2,len(time)))
print(x_ar)
for i in range(len(pos)):
    dt = time[i] - time_prev
    time_prev = time[i]
    A[1][0] = 0
    A_d = np.eye(2) + A*dt
    B_d = B*dt
    G[0] = 0
    G[1] = -mgl*np.sin(pos[i])/I

    x = G*dt + np.dot(A_d,x) + B_d*cur[i] + L*(pos[i] - x[0])
    #print(x)
    x_ar[0,i] = x[0]
    x_ar[1,i] = x[1]

plt.plot(time,pos,label="x")
plt.plot(time,vel,label="dx")
plt.plot(time,x_ar[0,:],label="x est")
plt.plot(time,x_ar[1,:],label="dx est")
plt.legend()
plt.show()
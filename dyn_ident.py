import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
data = np.genfromtxt('data.csv',delimiter = ',')

b,a = signal.butter(2,0.05)


time = data[:,0]
x = data[:,1]
x_f = signal.filtfilt(b,a,x)
vel = data[:,2]
cur = data[:,3]
dt = np.diff(time)
dx = np.diff(x_f)/dt
dx_f = signal.filtfilt(b,a,dx)
ddx = np.diff(dx_f)/dt[1:]
ddx_f = signal.filtfilt(b,a,ddx)
dx = dx[1:]
dx_f = dx_f[1:]
x = x[2:]
x_f = x_f[2:]
time = time[2:]
cur = cur[2:]

km = 0.03
m = 0.126
l = 0.15
g = 9.8

print(m*g*l)
X = np.array([ddx_f,dx_f])
coef = np.dot(km*cur-0.183*np.sin(x_f),np.linalg.pinv(X))
print(coef)

plt.plot(time,ddx,label="ddx")
plt.plot(time,ddx_f,label="ddx_f")
plt.plot(time,dx,label="dx")
plt.plot(time,dx_f,label="dx_f")
plt.plot(time,x,label="x")
plt.plot(time,x_f,label="x_f")
plt.legend()
plt.show()
plt.plot(time,cur,label="cur")
plt.plot(time,(0.183*np.sin(x_f) + 0.001*dx_f +  0.0040*ddx_f)/0.03,label="cur_calc")
plt.legend()
plt.show()
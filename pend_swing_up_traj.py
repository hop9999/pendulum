from pendulum import *
import matplotlib.pyplot as plt
import os
import time

bus = can.interface.Bus(bustype='socketcan',channel='can0',bitrate=1000000)
data_des = np.genfromtxt('opt_traj/swing_up.csv',delimiter=',').transpose()
motor = Actuator(0x141,bus)
pendulum = Pendulum(0.126,0.15)
N = 2001

proc_time = np.zeros(N)
X_ar = np.zeros((4,N))

q_des = np.pi/2
state = motor.get_state()
prev_time = state.time
for i in range(N):  
    while time.time() - prev_time < 0.0025:
        pass
    prev_time = time.time()
    X_des = np.array([[data_des[1,i]],
                      [data_des[2,i]],
                      [0]])

    X = state.X
    u =  data_des[3,i] + pendulum.cont_pd(X_des,X)
    proc_time[i] = state.time
    X_ar[0,i] = state.time
    X_ar[1:3,i] = state.X.reshape((1,2))
    X_ar[3,i] = state.current
    
    state = motor.send_current(u)

motor.send_current(0)

#np.savetxt("data_static.csv",np.transpose(X_ar),delimiter = ',')

plt.plot(proc_time,X_ar[1,],label="pos")
plt.plot(proc_time,X_ar[2,],label="vel")
plt.plot(proc_time,data_des[1,:],'--',label="x_des")
plt.plot(proc_time,data_des[2,:],'--',label="vel_des")
plt.legend()
plt.savefig("swing_up.png")

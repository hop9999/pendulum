from pendulum import *
import matplotlib.pyplot as plt
import os
import time

#param = os.sched_param(os.sched_get_priority_max(os.SCHED_FIFO))
#os.sched_setscheduler(0, os.SCHED_FIFO, param)
bus = can.interface.Bus(bustype='socketcan',channel='can0',bitrate=1000000)

motor = Actuator(0x141,bus)
pendulum = Pendulum(0.126,0.15)
N = 4000
time.sleep(2)
proc_time = np.zeros(N)
X_ar = np.zeros((4,N))

q_des = np.pi/2
state = motor.get_state()
prev_time = state.time
for i in range(N):  
    while time.time() - prev_time < 0.0025:
        pass
    prev_time = time.time()
    X_des = np.array([[q_des],
                      [0],
                      [0]])
    X = state.X
    u = pendulum.control_pd(X_des,X)
    proc_time[i] = state.time
    X_ar[0,i] = state.time
    X_ar[1:3,i] = state.X.reshape((1,2))
    X_ar[3,i] = state.current
    
    state = motor.send_current(u)

motor.send_current(0)

np.savetxt("data_static.csv",np.transpose(X_ar),delimiter = ',')
dt = np.diff(proc_time)
plt.plot(proc_time[1:],dt,label="dt")
plt.legend()
plt.savefig("dt.png")
plt.plot(proc_time[1:],X_ar[1,1:],label="pos")
plt.plot(proc_time[1:],X_ar[2,1:],label="vel")
plt.plot(proc_time[1:],q_des + 0*proc_time[1:],'--',label="x_des")
plt.legend()
plt.savefig("foo.png")

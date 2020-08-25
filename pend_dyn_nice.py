from pendulum import *
import os

param = os.sched_param(os.sched_get_priority_max(os.SCHED_FIFO))
os.sched_setscheduler(0,os.SCHED_FIFO,param)
bus = can.interface.Bus(bustype='socketcan',channel='can0',bitrate=1000000)

motor = Actuator(0x141,bus)
pendulum = Pendulum(0.126,0.15)
N = 4000

proc_time = np.zeros(N)
X_ar = np.zeros((4,N))


state = motor.get_state()
for i in range(N):  
    X_des = ident_traj(np.array([state.time]))
    X = state.X
    u = pendulum.control(X_des,X)
    proc_time[i] = state.time
    X_ar[0,i] = state.time
    X_ar[1:3,i] = state.X.reshape((1,2))
    X_ar[3,i] = state.current
    state = motor.send_current(u)

motor.send_current(0)
print(state.time)
np.savetxt("data_dyn.csv",np.transpose(X_ar),delimiter = ',')


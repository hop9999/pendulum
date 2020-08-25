from pendulum import *


bus = can.interface.Bus(bustype='socketcan',channel='can0',bitrate=1000000)

motor = Actuator(0x141,bus)
pendulum = Pendulum(0.126,0.15)
N = 40000

proc_time = np.zeros(N)
X_ar = np.zeros((4,N))

state = motor.get_state()
for i in range(N):  
    X_des = step_traj(state.time) 
    X = state.X
    u = pendulum.control(X_des,X)
    proc_time[i] = state.time
    X_ar[0,i] = state.time
    X_ar[1:3,i] = state.X.reshape((1,2))
    X_ar[3,i] = state.current
    state = motor.send_current(u)

motor.send_current(0)

np.savetxt("data_static.csv",np.transpose(X_ar),delimiter = ',')
#X_des = chirp_traj(a0,a,w0,nu,X_ar[1,0:])

dt = np.diff(proc_time)
vel_cal = np.diff(X_ar[0,:])/dt
plt.plot(proc_time[1:],X_ar[1,1:],label="pos")
plt.legend()
plt.show()

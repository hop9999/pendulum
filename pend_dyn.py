from pendulum import *
import matplotlib.pyplot as plt

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

np.savetxt("data_dyn.csv",np.transpose(X_ar),delimiter = ',')
X_des = ident_traj(proc_time)
#print(X_des)
#print(X_des[0,:])
dt = np.diff(proc_time)

plt.plot(proc_time[1:],dt)
plt.show()

vel_cal = np.diff(X_ar[0,:])/dt
plt.plot(proc_time[1:],X_ar[1,1:],label="pos")
plt.plot(proc_time[1:],X_ar[2,1:],label="vel")

plt.plot(proc_time[1:],X_des[0,1:],'--',label="x_des")
plt.plot(proc_time[1:],X_des[1,1:],'--',label="dx_des")
plt.legend()
plt.show()

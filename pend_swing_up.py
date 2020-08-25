from pendulum import *
import matplotlib.pyplot as plt

bus = can.interface.Bus(bustype='socketcan',channel='can0',bitrate=1000000)

motor = Actuator(0x141,bus)
pendulum = Pendulum(0.126,0.15)
N = 8000

proc_time = np.zeros(N)
X_ar = np.zeros((4,N))

X_des = np.array([[np.pi],
                      [0],
                      [0]])
state = motor.get_state()
for i in range(N):
    
    X = state.X
    E = pendulum.mgl*(1 - np.cos(X[0])) + pendulum.I*X[1]**2/2  
    k = 0.5
    if(E < 0.95*2*pendulum.mgl):
        u = k*X[1]
        #print(1)
    elif(E > 1.05*2*pendulum.mgl):
        u = -k*X[1]
        #print(-1)
    else:
        u = pendulum.control(X_des,X)
        #print(0)
    #print(E,2*pendulum.mgl)
    u = np.clip(u,-2,2)
    proc_time[i] = state.time
    X_ar[0,i] = state.time
    X_ar[1:3,i] = state.X.reshape((1,2))
    X_ar[3,i] = state.current
    state = motor.send_current(u)

motor.send_current(0)

plt.plot(X_ar[1,1:],X_ar[2,1:],label="vel")
plt.legend()
plt.show()

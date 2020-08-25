from actuator import *

def chirp_traj(a0,a,w0,nu,t):
    omega = 2*np.pi*(w0 + nu*t)
    x = a0 + a*np.sin(omega*t)
    dx = a*(omega + 4*np.pi*nu*t)*np.cos(omega*t)
    ddx = -a*(omega + 4*np.pi*nu*t)**2*np.sin(omega*t)
    return np.array([[x],
                     [dx],
                     [ddx]])

bus = can.interface.Bus(bustype='socketcan',channel='can0',bitrate=1000000)

motor = Actuator(0x141,bus)
N = 4000

proc_time = np.zeros(N)
X_ar = np.zeros((4,N))
a = np.pi/2
a0 = 0
w0 = 0.0
nu = 0.05

km = 0.03
m = 0.126
l = 0.15
g = 9.8

w = 0.41
h = 0.02

I = m*(w**2 + h**2)/12 + m*l**2

state = motor.get_state()
for i in range(N):  
    X_des = chirp_traj(a0,a,w0,nu,state.time)
             
    X = state.X

    K = np.array([[2, 0.2]])
    u = (m*g*l*np.sin(X_des[0]) + 0*I*X_des[2] + 0.0*X_des[1]+np.dot(K,X_des[0:2,:]-X))/km
    u = np.clip(u,-10,10)
    proc_time[i] = state.time
    X_ar[0,i] = state.time
    X_ar[1:3,i] = state.X.reshape((1,2))
    X_ar[3,i] = state.current
    state = motor.send_current(u[0][0])

motor.send_current(0)

np.savetxt("data.csv",np.transpose(X_ar),delimiter = ',')
X_des = chirp_traj(a0,a,w0,nu,X_ar[1,0:])

dt = np.diff(proc_time)
vel_cal = np.diff(X_ar[0,:])/dt
plt.plot(proc_time[1:],X_ar[1,1:],label="pos")
plt.plot(proc_time[1:],X_ar[2,1:],label="vel")
plt.legend()
plt.show()

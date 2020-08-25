from pendulum import *

time = np.linspace(0,10,1000)
X_des = ident_traj(time)
plt.plot(time[1:],X_des[0,1:],'--',label="x_des")
plt.plot(time[1:],X_des[1,1:],'--',label="dx_des")
plt.legend()
plt.show()

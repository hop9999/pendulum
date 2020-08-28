import numpy as np 

data_des = np.genfromtxt('opt_traj/swing_up.csv',delimiter=',').transpose()

print(np.size(data_des))
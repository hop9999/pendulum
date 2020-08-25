import numpy as np
from scipy import linalg 

A = np.array([[0, 1],
              [-1, 0]])

B = np.array([[0],
              [1]])

Q = np.array([[10, 0],
              [0, 1]])

R = np.array([[1]])

dt = 1e-2

def discr_lqr(A,B,Q,R,dt):
    A_d = np.eye(2) + A*dt
    B_d = B*dt
    S = linalg.solve_discrete_are(A_d, B_d, Q, R)
    K = np.dot(linalg.pinv(R + np.dot(np.dot(B_d.transpose(),S),B_d)),np.dot(np.dot(B_d.transpose(),S),A_d))
    #E,V = linalg.eig(A_d-B_d*K)
    return K

def cont_lqr(A,B,Q,R,dt):
    Scon = linalg.solve_continuous_are(A, B, Q, R)
    K = np.dot(np.dot(linalg.pinv(R),B.transpose()),Scon)
    #E,V = linalg.eig(A-B*K)
    return K

A_d = np.eye(2) + A*dt
B_d = B*dt
S = linalg.solve_discrete_are(A_d, B_d, Q, R)
K = np.dot(linalg.pinv(R + np.dot(np.dot(B_d.transpose(),S),B_d)),np.dot(np.dot(B_d.transpose(),S),A_d))
E,V = linalg.eig(A_d-B_d*K)    
print(S)
print("discr",K)
print(E)

Scon = linalg.solve_continuous_are(A, B, Q, R)
K = np.dot(np.dot(linalg.pinv(R),B.transpose()),Scon)
E,V = linalg.eig(A-B*K)
print(Scon)
print("cont",K)
print(E)
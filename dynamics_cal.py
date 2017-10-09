import numpy as np
import matplotlib.pyplot as plt
import random
from config import *
import stiffness_pick as sp


for k, v in configs.items():
    exec('%s=%s' % (k, v))

T = np.arange(0, tn, dt)
pt = lambda p:p['A']*np.sin(p['w']*T+random.uniform(0, 2*np.pi))
P = np.array([sum([pt(Pxi)for Pxi in Px]), sum([pt(Pzi)for Pzi in Pz])]).T
M = np.eye(2)*np.array([mx, mz])
X = np.zeros((1, 2))
V = np.zeros((1, 2))
A = np.zeros((1, 2))

for i, t in enumerate(T):
    if t*10%1==0:print('Calculation in %ss' % t)
    K = sp.K(*X[-1])
    C = 2*zeta*np.sqrt(M*K)
    A = np.vstack((A, np.dot((P[i]-np.dot(K, X[-1])-np.dot(C, V[-1])),np.linalg.inv(M).T)))
    V = np.vstack((V, A[-1]*dt))
    X = np.vstack((X, V[-1]*dt))
    # print('K=%s\nX=%s\nV=%s\nA=%s'%(K, X, V, A))

lX = X.T
lim = max(max(lX[0], key=np.abs), max(lX[1], key=np.abs))
plt.figure(figsize=(6,6))
plt.xlim(-lim, lim)
plt.ylim(-lim, lim)
plt.scatter(lX[0], lX[1], c=range(len(lX[0])))
plt.show()
    

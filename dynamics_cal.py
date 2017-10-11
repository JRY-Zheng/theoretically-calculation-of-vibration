import numpy as np
import matplotlib.pyplot as plt
import random
import stiffness_pick as sp

def dy_cal(cnf, n=0):
    print('Begin NO.%s dynamics calculation...' % n)
    T = np.arange(0, cnf.tn, cnf.dt)
    pt = lambda p:p['A']*np.sin(p['w']*T+random.uniform(0, 2*np.pi))
    P = np.array([sum([pt(Pxi)for Pxi in cnf.Px]), sum([pt(Pzi)for Pzi in cnf.Pz])]).T
    M = np.eye(2)*np.array([cnf.mx, cnf.mz])
    X = np.zeros((1, 2))
    V = np.zeros((1, 2))
    A = np.zeros((1, 2))

    for i, t in enumerate(T):
        # if t*10%1==0:print('Calculation in %ss' % t)
        K = sp.K(*X[-1])
        C = 2*cnf.zeta*np.sqrt(M*K)
        A = np.vstack((A, np.dot((P[i]-np.dot(K, X[-1])-np.dot(C, V[-1])),np.linalg.inv(M).T)))
        V = np.vstack((V, A[-1]*cnf.dt))
        X = np.vstack((X, V[-1]*cnf.dt))
        # print('K=%s\nX=%s\nV=%s\nA=%s'%(K, X, V, A))

    lX = X.T
    t_lim = max(lX[0]), max(lX[1])
    # lim = max(*t_lim)
    # plt.figure(figsize=(6,6))
    # plt.xlim(-lim, lim)
    # plt.ylim(-lim, lim)
    # plt.scatter(lX[0], lX[1], c=range(len(lX[0])))
    # plt.show()
    print('Succeed in NO.%s dynamics calculation.' % n)
    return t_lim

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
##from config import *
##
##for k, v in configs.items():
##    exec('%s=%s' % (k, v))

def stf_cal(cnf, n=0):
    print('Begin NO.%s stiffness calculating...' % n)
    # x, z以右上角为正
    lx = np.linspace(0, cnf.xm, cnf.N)
    lz = np.linspace(0, cnf.zm, cnf.N)
    x, z = np.meshgrid(lx, lz)

    # 力增量以右上角为正
    Ch = -z/cnf.Lh
    Cv = -x/cnf.Lv

    # v, h分别代表水平方向、垂直方向的力（由竖直、水平的扭簧产生）
    Fv = cnf.Kv*Cv
    Fh = cnf.Kh*Ch
    Fv0 = cnf.Kv*cnf.Cv0
    Fh0 = cnf.Kh*cnf.Ch0

    Fx = Fv*np.cos(Ch)
    Fzx = -(Fv+Fv0)*np.sin(Ch)
    Fzz = Fh*np.cos(Ch)

    x[x==0] = float('inf')
    z[z==0] = float('inf')
    K = np.dstack((np.dstack((-Fx/x, np.zeros((len(lx) ,len(lz))))), np.dstack((-Fzx/x, -Fzz/z))))

    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # cax = ax.matshow(Kx)
    # fig.colorbar(cax)
    # plt.show()

    K = K.tolist()
    for i, Ki in enumerate(K):
        for j, Kj in enumerate(Ki):
            K[i][j] = np.array(Kj)
    datK = pd.DataFrame(K)
    datK.columns = lx
    datK['Z'] = lz
    datK.to_csv('stiffness.csv')
    print('Succeed in NO.%s stiffness calculation.' % n)

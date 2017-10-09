import pandas as pd
import numpy as np
import os


class ResultNullError(IOError):
    ERROR = ('Stiffness result is invalid. Run the stiffness_cal.py',)

class ResultInvalidError(ValueError):
    ERROR = ('Vibration is over the former stifness calculation region.',)

for i in range(2):
    if not os.path.exists('stiffness%s.csv' % i):
        raise ResultNullError(ResultNullError.ERROR[0])
    exec('dfK%s = pd.read_csv("stiffness%s.csv")' % (i, i))
    exec('datK%s, c%s = dfK%s.values, dfK%s.columns' % (i, i, i, i))


def trans(l, key):
    nl = []
    for li in l:
        try:
            nli = key(li)
        except:
            nli = False
        nl.append(nli)
    return np.array(nl)


def K(x, z, datK, c):
    x, z = np.abs(x), np.abs(z)
    if not datK[datK[:][-1]<=z].any():
        raise ResultInvalidError(ResultInvalidError[0])
    Kt = max(datK[trans(datK, lambda p:p[-1]<=z)], key=lambda p:p[-1])
    Kb = min(datK[trans(datK, lambda p:p[-1]>=z)], key=lambda p:p[-1])
    tc = trans(c, float)[1:-1]
    Kl = np.argmax(tc[tc<=x])
    Kr = Kl+1
    # print(Kr, Kl, Kt, Kb)
    if len(Kb)==0 or Kr==len(Kb):
        raise ResultInvalidError(ResultInvalidError[0])
    lt = Kt[Kl]
    rt = Kb[Kl]
    lb = Kt[Kr]
    rb = Kb[Kr]
    dh = tc[Kr]-tc[Kl]
    dv = Kb[-1]-Kt[-1]
    lt *= (x-tc[Kl])/dh if dh!=0 else 1
    rt *= (tc[Kr]-x)/dh if dh!=0 else 1
    lb *= (x-tc[Kl])/dh if dh!=0 else 1
    rb *= (tc[Kr]-x)/dh if dh!=0 else 1
    lt *= (z-Kt[-1])/dv if dv!=0 else 1
    rt *= (z-Kt[-1])/dv if dv!=0 else 1
    lb *= (Kb[-1]-z)/dv if dv!=0 else 1
    rb *= (Kb[-1]-z)/dv if dv!=0 else 1
    return lt+lb+rt+rb


def Kx(x, z):
    return K(x, z, datK0, c0)


def Kz(x, z):
    return K(x, z, datK1, c1)

import pandas as pd
import numpy as np
import os


class ResultNullError(IOError):
    ERROR = ('Stiffness result is invalid. Run the stiffness_cal.py',)

class ResultInvalidError(ValueError):
    ERROR = ('Vibration is over the former stifness calculation region.',)

def trans(l, key):
    nl = []
    for li in l:
        try:
            nli = key(li)
        except:
            nli = False
        nl.append(nli)
    return np.array(nl)

def str2arr(s):
    return np.array(trans(s[1:-1].split(), key=float)).reshape((2,2))

def K(x, z, n=0):
    if not os.path.exists('stiffness\stiffness%s.csv' % n):
        raise ResultNullError(ResultNullError.ERROR[0])
    dfK = pd.read_csv('stiffness\stiffness%s.csv' % n)
    datK, c = dfK.values, dfK.columns
    x, z = np.abs(x), np.abs(z)
    if not datK[trans(datK[:].T[-1], float)<=z].any():
        raise ResultInvalidError(ResultInvalidError[0])
    Kt = max(datK[trans(datK, lambda p:float(p[-1])<=z)], key=lambda p:float(p[-1]))
    Kb = min(datK[trans(datK, lambda p:float(p[-1])>=z)], key=lambda p:float(p[-1]))
    tc = trans(c, float)[1:-1]
    Kl = max(np.argmax(tc[tc<=x]), 1)
    Kr = Kl+1
    # print(Kr, Kl, Kt, Kb)
    if len(Kb)==0 or Kr==len(Kb):
        raise ResultInvalidError(ResultInvalidError[0])
    lt = str2arr(Kt[Kl])
    rt = str2arr(Kb[Kl])
    lb = str2arr(Kt[Kr])
    rb = str2arr(Kb[Kr])
    dh = tc[Kr]-tc[Kl]
    dv = Kb[-1]-Kt[-1]
    dh0 = dh!=0
    dv0 = dv!=0
    lt *= (x-tc[Kl])/dh if dh0 else 1
    rt *= (tc[Kr]-x)/dh if dh0 else 1
    lb *= (x-tc[Kl])/dh if dh0 else 1
    rb *= (tc[Kr]-x)/dh if dh0 else 1
    lt *= (z-Kt[-1])/dv if dv0 else 1
    rt *= (z-Kt[-1])/dv if dv0 else 1
    lb *= (Kb[-1]-z)/dv if dv0 else 1
    rb *= (Kb[-1]-z)/dv if dv0 else 1
    return lt+lb+rt+rb

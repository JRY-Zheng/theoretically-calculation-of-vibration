#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Default configurations.
'''

__author__ = 'J.R.Y Zheng'

configs = {
    'Lh':5,
    'Lv':5,
    'Kh':1,
    'Kv':1,
    'Ch0':1,
    'Cv0':1,
    'xm':0.1,
    'zm':0.2,
    'N':101,
    #-------
    'tn':10**0,
    'dt':10**(-3),
    'mx':1,
    'mz':1,
    'Px':[
        {'A':0.1, 'w':100},
        {'A':0.1, 'w':1000}
        ],
    'Pz':[
        {'A':1, 'w':100},
        {'A':0.5, 'w':1000}
        ],
    'zeta':0.1
}

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, re

class ItemCountConflictError(ValueError):
    ERROR = ('Count of column is not match!', 'Count of keyword is not match!')

class table:
    data = []
    column = []
    keyword = []
    def __init__(self, data=[], column=[], keyword=[]):
        if len(data)!=len(keyword):raise ItemCountConflictError(ItemCountConflictError.ERROR[1])
        if len(data)!=0 and len(data[0])!=len(column):raise ItemCountConflictError(ItemCountConflictError.ERROR[0])
        self.data = data
        self.column = column
        self.keyword = keyword
    def search(self, column = [], keyword = []):
        column = self.column if column==[]else column
        keyword = self.keyword if keyword==[]else keyword
        return [[self.data[k][c]for c in [self.column.index(i)for i in column]]for k in [self.keyword.index(j)for j in keyword]]
    def add(self, data, column = [], keyword = [], default = 0):
        column = self.column if column==[]else column
        keyword = self.keyword if keyword==[]else keyword
        if len(data)!=len(keyword):raise ItemCountConflictError(ItemCountConflictError.ERROR[1])
        if len(data[0])!=len(column):raise ItemCountConflictError(ItemCountConflictError.ERROR[0])
        new_column_index = [column.index(i)for i in list(set(column).difference(set(self.column)))]
        old_column_index = list(set(range(len(column))).difference(set(new_column_index)))
        new_keyword_index = [keyword.index(i)for i in list(set(keyword).difference(set(self.keyword)))]
        old_keyword_index = list(set(range(len(keyword))).difference(set(new_keyword_index)))
        for i in old_column_index:
            for j in old_keyword_index:
                self.data[self.keyword.index(keyword[j])][self.column.index(column[i])]=data[j][i]
        for j in new_keyword_index:
            self.keyword.append(keyword[j])
            self.data.append([default for k in range(len(self.column))])
            for i in old_column_index:
                self.data[-1][self.column.index(column[i])]=data[j][i]
        for i in new_column_index:
            self.column.append(column[i])
            [k.append(default)for k in self.data]
            for j in old_keyword_index:
                self.data[self.keyword.index(keyword[j])][-1]=data[j][i]
        for i in new_column_index:
            for j in new_keyword_index:
                self.data[self.keyword.index(keyword[j])][self.column.index(column[i])]=data[j][i]
        

insp = table()
dire = ['center', 'lefttop', 'righttop', 'leftbottom', 'rightbottom']

for pn, dn, fn in os.walk('inspiration/'):
    for f in fn:
        for d in dire:
            fm = re.match(d+r'-(\d+).txt', f)
            if not fm: continue
            insp.add(data=[[pd.read_csv(pn+f).values.T]],column=[fm[1]],keyword=[d])
            break
        

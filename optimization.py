# -*-coding:utf-8 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from random import *
import time

sz = 20  # 计算精度/规模
boundary = 4

# START = time.time()
# # 这一部分是生成全部数据，用以计算真实的最大值。实际优化过程中这一部分是不可取的。
# x = np.arange(-boundary, boundary, boundary/2**(sz+5))
# y = np.arange(-boundary, boundary, boundary/2**(sz+5))
# x, y = np.meshgrid(x, y)  # 由两个[1, 2]变为[[1,2],[1,2]]和[[1,1],[2,2]]


def cal(a, b):
    return np.sin(np.sqrt(a**2+b**2))+np.sin(np.sqrt((a-3)**2+(b-3)**2))
# z = cal(x, y)
#
# print(max(max(z, key=max)))
END = time.time()
# print('It used:%s s' % '{00}'.format(END-START))
START = END

# 这段注释去的代码可以显示函数的真实图形
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# img = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='rainbow')
# plt.show()

# 定义常数以减小计算量
div = 2  # 将45°n等分
sin = [np.sin(i*np.pi/div/4)for i in range(8*div)]
cos = sin[2*div:]+sin[:2*div]
sin.append(0)
cos.append(0)
# 生成第一批随机数据点，在空间内均匀分布，并排序生成新列。二者的数据均为整型的坐标，即坐标在x, y中的序号
climber = [[uniform(-boundary, boundary) for grid in range(2)]for i in range(sz)]
option = []

# 动态生成需要记录的数据列
for pn in ('px', 'py', 'pz', 'pc'):
    exec('%s=[]' % pn)

process = 0  # 记录优化过程的进展
best_result = [[0, 0], 0]  # 记录最佳优化结果

while(True):
    # 记录必要数据以便绘图
    [px.append(clm[0])for clm in climber]
    [py.append(clm[1])for clm in climber]
    [pz.append(cal(clm[0], clm[1]))for clm in climber]
    [pc.append(process)for clm in climber]
    option.clear()
    # 计算各个方向的值
    [option.append([[boundary*sin[phi]/(process+sz*2)+clm[0], boundary*cos[phi]/(process+sz*2)+clm[1]]
                    for phi in range(8*div+1)])for clm in climber]
    climber.clear()
    # 比较各方向和自身，选取其中最优者为下一次更新的状态
    [climber.append(max(opt, key=lambda tp: cal(*tp)))for opt in option]
    best_result[0] = max(climber, key=lambda tp: cal(*tp))
    best_result[1], temp = cal(*best_result[0]), best_result[1]
    process += 1
    if best_result[1] == temp:
        break

# 打印最终结果
print('(%s, %s): %s' % (best_result[0][0], best_result[0][1], best_result[1]))
END = time.time()
print('It used:%s s' % '{00}'.format(END-START))
START = END
# 显示结果收敛的过程图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
img = ax.scatter(px, py, pz, c=pc)
plt.colorbar(img)
plt.show()

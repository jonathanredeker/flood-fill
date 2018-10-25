import numpy as np
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D

"""
The purpose of this file is to aid debugging of the 3D Flood Fill.
"""

collision_map = [[[2,1,0,0,0],
                  [1,1,1,0,0],
                  [1,0,1,0,0],
                  [1,0,0,0,0]],
                 [[0,1,0,0,0],
                  [0,1,1,0,0],
                  [0,0,1,0,0],
                  [1,0,0,0,0]],
                 [[0,1,0,0,0],
                  [0,1,1,0,0],
                  [0,0,1,0,0],
                  [1,0,0,0,0]]]

length = len(collision_map[0][0])
width = len(collision_map[0])
height = len(collision_map)

obstacles = np.zeros((height, width, length), dtype=int)

path = [[4, 3, 2], [3, 3, 1], [2, 3, 0], [1, 2, 0], [0, 1, 1], [0, 0, 0]]
x = []
y = []
z = []

for coordinate in path:
    z.append(coordinate[2])
    y.append(coordinate[1])
    x.append(coordinate[0])

for dz in range(len(collision_map)):
    for dy in range(len(collision_map[dz])):
        for dx in range(len(collision_map[dz][dy])):
            if collision_map[dz][dy][dx] == 0 or collision_map[dz][dy][dx] == 1:
                obstacles[dz][dy][dx] = collision_map[dz][dy][dx]
            else:
                obstacles[dz][dy][dx] = 0

z2, y2, x2 = obstacles.nonzero()

print obstacles
print path

figure = plot.figure()
ax = figure.add_subplot(111, projection='3d', title="Solved Path & Obstacles")

ax.plot(x, y, z, c="b", marker=".")
ax.plot([x[0]], [y[0]], [z[0]], c="g", marker="o")
ax.plot([x[-1]], [y[-1]], [z[-1]], c="r", marker="X", markersize=8)
ax.scatter(x2, y2, z2, c="black", marker="s")

plot.show()

import turtle
import math
import numpy as np
from copy import copy, deepcopy


turtle.bgcolor('#00010d')
turtle.tracer(0)
turtle.hideturtle()
turtle.pen(pencolor="#fff3de", pensize=3)
turtle.penup()


def X_ROTATION(theta_x):
    rotation = [
        [1, 0, 0],
        [0, math.cos(theta_x), -math.sin(theta_x)],
        [0, math.sin(theta_x), math.cos(theta_x)]
    ]
    return rotation


def Z_ROTATION(theta_z):
    rotation = [
        [math.cos(theta_z), -math.sin(theta_z), 0],
        [math.sin(theta_z), math.cos(theta_z), 0],
        [0, 0, 1]
    ]
    return rotation


def Y_ROTATION(theta_y):
    rotation = [
        [math.cos(theta_y), 0, math.sin(theta_y)],
        [0, 1, 0],
        [-math.sin(theta_y), 0, math.cos(theta_y)]
    ]
    return rotation


class Toroid:
    def __init__(self, R1, R2):
        self.points = []
        self.surface_normals = []
        self.light = [0, 1, -1]
        self.DISTANCE = 40000
        cos = math.cos
        sin = math.sin
        phi = 0

        while phi <= 360:
            theta = 0
            circle_points = []
            normal_points = []
            y_rotate_phi = Y_ROTATION(phi)

            while theta <= 360:
                circle_points.append((R2+R1*cos(theta), R1*sin(theta), 0))
                normal_points.append((cos(theta), sin(theta), 0))
                theta = theta + 7.2

            for point in circle_points:
                self.points.append(tuple(np.matmul(point, y_rotate_phi)))

            for point in normal_points:
                self.surface_normals.append(
                    tuple(np.matmul(point, y_rotate_phi)))

            phi = phi + 7.2

    def in_2D(self, depth):
        twoD_points = []
        for point in self.points:
            x, y, z = point
            twoD_points.append((x*depth/(z+depth), y*depth/(z+depth)))
        return twoD_points

    def luminance(self):
        L = []
        for normal in self.surface_normals:
            L.append(np.dot(normal, self.light))
        return L

    def update_y(self, theta_y):
        y_rotate = Y_ROTATION(theta_y)
        for i in range(len(self.points)):
            point = self.points[i]
            self.points[i] = tuple(np.matmul(point, y_rotate))

        for i in range(len(self.surface_normals)):
            point = self.surface_normals[i]
            self.surface_normals[i] = tuple(np.matmul(point, y_rotate))

    def update_x(self, theta_x):
        x_rotate = X_ROTATION(theta_x)
        for i in range(len(self.points)):
            point = self.points[i]
            self.points[i] = tuple(np.matmul(point, x_rotate))

        for i in range(len(self.surface_normals)):
            point = self.surface_normals[i]
            self.surface_normals[i] = tuple(np.matmul(point, x_rotate))

    def draw_shape(self):
        turtle.penup()
        points = self.in_2D(400)
        luminances = self.luminance()

        for point, lum in zip(points, luminances):
            turtle.goto(*point)
            if lum > 0:
                turtle.dot(size=5*lum)

    def return_points(self):
        return self.points

    def update_points(self, new_points):
    		self.points = new_points

    def return_surface_normals(self):
            return self.surface_normals

    def update_surface_normals(self, new_normals):
    		self.surface_normals = new_normals


shape = Toroid(50, 100)

store_points = []
store_normals = []

for i in range(100):
    shape.update_y(.09)
    shape.update_x(.18)
    store_points.append(deepcopy(shape.return_points()))
    store_normals.append(deepcopy(shape.return_surface_normals()))

i = 0
while True:
    turtle.clear()
    shape.draw_shape()
    shape.update_points(store_points[i])
    shape.update_surface_normals(store_normals[i])
    i = (i + 1) % 99
    turtle.update()

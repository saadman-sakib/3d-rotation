import turtle
import math
import numpy as np


turtle.bgcolor('#00010d')
turtle.tracer(0)
turtle.hideturtle()
turtle.pen(pencolor="#fff3de", pensize=3)


class P:
	def __init__(self,x,y,z):
		self.x = x
		self.y = y
		self.z = z

	#2d projection of 3D points
	def in_2d(self, depth):
		x = self.x
		y = self.y
		z = self.z
		return(x*depth/(z+depth), y*depth/(z+depth))


class Box():
	def __init__(self):
		self.DISTANCE = -40000
		EDGE = 200
		self.threeD_points = [
			(0,0,-EDGE/2),
			(EDGE,0,-EDGE/2),
			(EDGE,EDGE,-EDGE/2),
			(0,EDGE,-EDGE/2),
			(0,0,EDGE/2),
			(EDGE,0,EDGE/2),
			(EDGE,EDGE,EDGE/2),
			(0,EDGE,EDGE/2)
		]
		self.points = []

		for x in self.threeD_points:
			self.points.append(P(*x).in_2d(-self.DISTANCE))

	def draw_shape(self):
		points = self.points

		# square 1
		turtle.penup()
		turtle.goto(points[0])
		turtle.pendown()
		for i in range(1,4):
			turtle.goto(points[i])
		turtle.goto(points[0])

		# square 1
		turtle.penup()
		turtle.goto(points[4])
		turtle.pendown()
		for i in range(5,8):
			turtle.goto(points[i])
		turtle.goto(points[4])

		# connect rest of the points
		turtle.penup()
		for i in range(4):
			turtle.goto(points[i])
			turtle.pendown()
			turtle.goto(points[i+4])
			turtle.penup()

	def update_z(self, theta_z):
		transformation = [
			[math.cos(theta_z),-math.sin(theta_z),0],
			[math.sin(theta_z), math.cos(theta_z),0],
			[0,0,1]
		]

		for i in range(len(self.threeD_points)):
			point = self.threeD_points[i]
			self.threeD_points[i] = tuple(np.matmul(
									point,
									transformation
								))

		self.points = []
		for x in self.threeD_points:
			self.points.append(P(*x).in_2d(-self.DISTANCE))

	def update_x(self, theta_x):
		transformation = [
			[1,0,0],
			[0,math.cos(theta_x),-math.sin(theta_x)],
			[0, math.sin(theta_x),math.cos(theta_x)]
		]

		for i in range(len(self.threeD_points)):
			point = self.threeD_points[i]
			self.threeD_points[i] = tuple(np.matmul(
									point,
									transformation
								))
		self.points = []
		for x in self.threeD_points:
			self.points.append(P(*x).in_2d(-self.DISTANCE))


shape  = Box()

while True:
	turtle.clear()
	turtle.goto((0,0))
	turtle.pen(pencolor="#cf465d", pensize=3)
	turtle.dot(size=20)
	turtle.pen(pencolor="#fff3de", pensize=3)
	shape.draw_shape()
	shape.update_z(45)
	shape.update_x(.0021)
	shape.update_z(-45.0006)
	turtle.update()


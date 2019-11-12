#!/usr/bin/env python
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from master_msgs.msg import rpm, current,pots,sensibility
from master_msgs.msg import traction_Orders,connection,arm_Orders
import math
import rospy
import time
import matplotlib.pyplot as plt
from random import random

#j0,j1,j2,j3,j4,j5,j6 = 0.0,0.0,0.0,0.0,0.0,0.0,0.0
#v0,v1,v2,v3,v4,v5,v6 = 0.1,0.1,0.1,0.1,0.1,0.1,0.1
#an = [0,0,0,0,0,0] # Angles
#st = [100,0,0,0,0,0] # Steps
#stAng = 1.8
posAct = [0,-1.5,2.2,0,2,0] # Posición Inicial

#pots_present = pots()
actual_J = [0.0,0.0,0.0,0.0,0.0,0.0]
actual_V = [0.0,0.0,0.0,0.0,0.0,0.0]
t = []
pos = [[],[],[],[],[],[]]
vel = [[],[],[],[],[],[]]
#pos0,pos1,pos2,pos3,pos4,pos5 = [],[],[],[],[],[]
st,et = 0,0

def joints_Callback(param):
	global actual_J,actual_V
	try:
		for i in range(0,6):
			actual_J[i] = round(param.position[i],2)
			actual_V[i] = round(param.velocity[i],2)
	except:
		pass
	#print('JJ:',actual_J)
	#print(et)
	#plt.plot(et,actual_J[0])
	#plt.pause(1e-6)

def ruido():
	num = round((random()/50)-0.05,2)
	return num

def agregarRuido():
	global posAct
	global actual_J
	vec = [0,0,0,0,0,0]
	for i in range(0,6):
		r = ruido()
		vec[i] = actual_J[i]+r
	return vec

def getPos():
	global actual_J,pos
	for i in range(0,6):
		# pos.append(1)
		pos[i].append(actual_J[i])
	# print(pos)

def plotPos():
	global t,pos
	plt.clf()
	plt.suptitle('Positions')
	ax1 = plt.subplot(6,1,1)
	ax2 = plt.subplot(6,1,2)
	ax3 = plt.subplot(6,1,3)
	ax4 = plt.subplot(6,1,4)
	ax5 = plt.subplot(6,1,5)
	ax6 = plt.subplot(6,1,6)
	ax1.plot(t,pos[0],color='b')
	ax2.plot(t,pos[1],color='b')
	#plt.subplot(611)
	# for i in range(0,6):
	# 	a = int('61'+str(i+1))
	# 	plt.subplot(a)
	# 	plt.plot(t,pos[i],color='b')
	# 	#plt.title('Joint '+str(i)+':')
	plt.pause(0.05)

def getVel():
	global actual_V,vel
	for i in range(0,6):
		vel[i].append(actual_V[i])

def plotVel():
	global t,vel
	plt.suptitle('Velocities')
	for i in range(0,6):
		a = int('61'+str(i+1))
		plt.subplot(a)
		plt.plot(t,vel[i],color='b')
		#plt.title('Joint '+str(i)+':')
	plt.pause(0.05)

def armMain():
	global posAct
	global actual_J,pos
	global t,st,et
	#global pos0,pos1,pos2,pos3,pos4,pos5
	#actual_J = posAct
	rospy.init_node('sim_arm')
	rospy.Subscriber ('joint_states',JointState,joints_Callback)
	pub = rospy.Publisher('joint_states',JointState, queue_size=10)
	rate = rospy.Rate(10) # 10hz
	st = time.time()
	#plt.plot(t,pos)
	#plt.subplot(611)
	#ax1 = plt.subplot(6,1,1)

	plt.show()
	plt.clf()
	while not rospy.is_shutdown():
		v = agregarRuido()
		hello_str = JointState()
		hello_str.header = Header()
		hello_str.header.stamp = rospy.Time.now()
		hello_str.name = ['robocol_joint1','robocol_joint2',\
		'robocol_joint3','robocol_joint4','robocol_joint5','robocol_joint6']
		hello_str.position = v
		#hello_str.position = [actual_J0,actual_J1,actual_J2,\
		#actual_J3,j4,actual_J5]
		hello_str.velocity = [0,0,0,0,0,0]
		hello_str.effort = [0,0,0,0,0,0]
		hello_str.header.stamp = rospy.Time.now()
		#pub.publish(hello_str)
		et = round(time.time()-st,3)
		t.append(et)
		getPos()
		plotPos()
		#plt.plot([1,2],[1,2],color='b')
		#plt.show()
		#getVel()
		#plotVel()
		#pos0.append(actual_J[0])
		#pos1.append(actual_J[1])
		#pos2.append(actual_J[2])
		#pos3.append(actual_J[3])
		#pos4.append(actual_J[4])
		#pos5.append(actual_J[5])
		
		# plt.subplot(611)
		# plt.scatter(t,pos0,color='b')
		# plt.subplot(612)
		# plt.scatter(t,pos1,color='b')
		# plt.subplot(613)
		# plt.scatter(t,pos2,color='b')
		# plt.subplot(614)
		# plt.scatter(t,pos3,color='b')
		# plt.subplot(615)
		# plt.scatter(t,pos4,color='b')
		# plt.subplot(616)
		# plt.scatter(t,pos5,color='b')
		# plt.pause(0.05)
		rate.sleep()

if __name__ == '__main__':
	try:
		armMain()
	except rospy.ROSInterruptException:
		pass

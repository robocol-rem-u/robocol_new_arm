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

ini = 0
posIni = [0.0,-1.5,2.2,0.0,2.0,0.0] # Posición Inicial
actual_J,actual_V = [0.0,0.0,0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0,0.0,0.0]

# -------------------------------------------------------------
# --------------------- CALLBACKS -----------------------------
# -------------------------------------------------------------

def joints_Callback(param):
	global actual_J,actual_V
	try:
		for i in range(0,6):
			actual_J[i] = round(param.position[i],2)
			actual_V[i] = round(param.velocity[i],2)
	except:
		pass

def make_msg(pos,vel,eff):
	msg = JointState()
	msg.header = Header()
	msg.header.stamp = rospy.Time.now()
	msg.name = ['robocol_joint1','robocol_joint2',\
	'robocol_joint3','robocol_joint4','robocol_joint5','robocol_joint6']
	msg.position = pos
	msg.velocity = vel
	msg.effort = eff
	return msg

def fake_arm_control():
	global ini
	global posIni
	global actual_J,actual_V
	rospy.init_node('sim_arm')
	rospy.Subscriber ('joint_states',JointState,joints_Callback)
	pub = rospy.Publisher('joint_states',JointState, queue_size=10)
	rate = rospy.Rate(10) # 10hz
	ini = 1
	print('Inicializando...')
	while not rospy.is_shutdown():
		if actual_J == posIni and ini:
			ini = 0
			print("Posición Inicial Cargada.")
		if ini:
			print("Cargando Posición Inicial...")
			msg = make_msg(posIni,[0,0,0,0,0,0],[0,0,0,0,0,0])
		pub.publish(msg)
			# print("Inicializado correctamente.")
		# msg = JointState()
		# msg.header = Header()
		# msg.header.stamp = rospy.Time.now()
		# msg.name = ['robocol_joint1','robocol_joint2',\
		# 'robocol_joint3','robocol_joint4','robocol_joint5','robocol_joint6']
		# msg.position = posIni
		# msg.velocity = [0,0,0,0,0,0]
		# msg.effort = [0,0,0,0,0,0]
		rate.sleep()

if __name__ == '__main__':
	try:
		fake_arm_control()
	except rospy.ROSInterruptException:
		pass

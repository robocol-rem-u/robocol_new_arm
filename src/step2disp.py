#!/usr/bin/env python
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from master_msgs.msg import rpm, current,pots,sensibility
from master_msgs.msg import traction_Orders, connection, arm_Orders
import math
import rospy

j0,j1,j2,j3,j4,j5,j6 = 0.0,0.0,0.0,0.0,0.0,0.0,0.0
v0,v1,v2,v3,v4,v5,v6 = 0.1,0.1,0.1,0.1,0.1,0.1,0.1
an = [0,0,0,0,0,0] # Angles
st = [100,0,0,0,0,0] # Steps
stAng = 1.8

pots_present = pots()
actual_J0,actual_J1,actual_J2,actual_J3,actual_J4,actual_J5 = 0.0,0.0,0.0,0.0,0.0,0.0

def pots_Callback(param):
	global pots_present
	global actual_J0,actual_J1,actual_J2,actual_J3,actual_J4,actual_J5
	pots_present=param.J0
	actual_J0 = param.J0
	actual_J1 = param.J1
	actual_J2 = param.J2
	actual_J3 = param.J3
	actual_J4 = param.J4
	actual_J5 = param.J5

def calc_steps():
	global stAng
	global an # Angles
	global st # Steps
	for i in range(0,6):
		ang = st[i]*stAng
		print('A'+str(i)+':',ang)
	print(' ')

def step():


def stepsMain():
	rospy.init_node('mov2step')
	rospy.Subscriber ('topic_pots',pots,pots_Callback)
	#pub = rospy.Publisher('joint_states',JointState, queue_size=10)
	rate = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		hello_str = JointState()
		hello_str.header = Header()
		hello_str.header.stamp = rospy.Time.now()
		hello_str.name = ['robocol_joint1','robocol_joint2','robocol_joint3',\
		'robocol_joint4','robocol_joint5','robocol_joint6']
		#calc_steps()
		rate.sleep()

if __name__ == '__main__':
	try:
		stepsMain()
	except rospy.ROSInterruptException:
		pass

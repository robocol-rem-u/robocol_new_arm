#!/usr/bin/env python
import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import JointState
from master_msgs.msg import pots
from moveit_msgs.msg import MotionPlanRequest
#from master_msgs.msg import rpm, current,pots,sensibility
#from master_msgs.msg import traction_Orders, connection, arm_Orders
#import math

#pots_present = pots()
a = 0
pot_pos = [0.0,0.0,0.0,0.0,0.0,0.0]
sim_pos = [0.0,0.0,0.0,0.0,0.0,0.0]

def pots_Callback(param):
	global pots_present
	pot_pos[0] = param.J0
	pot_pos[1] = param.J1
	pot_pos[2] = param.J2
	pot_pos[3] = param.J3
	pot_pos[4] = param.J4
	pot_pos[5] = param.J5

def joints_Callback(param):
	global sim_pos
	sim_pos[0] = round(param.position[0],2)
	sim_pos[1] = round(param.position[1],2)
	sim_pos[2] = round(param.position[2],2)
	sim_pos[3] = round(param.position[3],2)
	sim_pos[4] = round(param.position[4],2)
	sim_pos[5] = round(param.position[5],2)

def motion_Callback(param):
	print(param)

def main():
	global pot_pos,a
	global sim_pos
	rospy.init_node('realArm_Control')
	rospy.Subscriber ('topic_pots',pots,pots_Callback)
	rospy.Subscriber ('joint_states',JointState,joints_Callback)
	rospy.Subscriber ('feedback',MotionPlanRequest,motion_Callback)
	pub = rospy.Publisher('joint_states', JointState, queue_size=10)
	pub = rospy.Publisher('topic_pots',pots, queue_size=10)
	rate = rospy.Rate(10) # 10hz
	while not rospy.is_shutdown():
		#print(sim_pos)
		# print(pot_pos)
		# try:
		# 	t = int(input("Pots?"))
		# 	s = pots()
		# 	s.header = Header()
		# 	s.header.stamp = rospy.Time.now()
		# 	s.J0 = t
		# 	pub.publish(s)
		# except Exception as e:
		# 	pass
		# hello_str = JointState()
		# hello_str.header = Header()
		# hello_str.header.stamp = rospy.Time.now()
		# hello_str.name = ['robocol_joint1','robocol_joint2','robocol_joint3','robocol_joint4','robocol_joint5','robocol_joint6']
		rate.sleep()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass

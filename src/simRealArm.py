#!/usr/bin/env python
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

# joints = JointState()

# -------------------------------------------------------------
# --------------------- CALLBACKS -----------------------------
# -------------------------------------------------------------
# # Joints State Callback.
# def joints_Callback(param):
# 	print(param)
# 	# pass
# # Move Group Feedback Callback.
# def feedback_Callback(param):
# 	pass
# # Move Group Trajectory Callback.
# def trajectory_Callback(param):
# 	pass



def sim_real_arm():
	global joints
	print('Simulating arm connected...')
	rospy.init_node('sim_real_arm')
	# rospy.Subscriber('joint_states',JointState,joints_Callback)
	# rospy.Subscriber('/move_group/feedback',MoveGroupActionFeedback,feedback_Callback)
	# rospy.Subscriber('/move_group/display_planned_path',DisplayTrajectory,trajectory_Callback)
	# --- PUBLISHERS --- #
	pub_Joints = rospy.Publisher('/joint_states',JointState,queue_size=10)
	# pub_Arm_Orders = rospy.Publisher('topic_arm_orders',arm_Orders,queue_size=10)
	# pub_Arm_Status = rospy.Publisher('topic_arm_status',arm_auto_status,queue_size=10)
	n = 0
	rate = rospy.Rate(5) # 1 Hz
	while not rospy.is_shutdown():
		if n < 10:
			print(' Publishing resting pose...')
			joints = JointState()
			joints.header = Header()
			joints.header.stamp = rospy.Time.now()
			joints.name = ['robocol_joint1','robocol_joint2','robocol_joint3','robocol_joint4','robocol_joint5','robocol_joint6','robocol_finger_joint1']
			# pose = 
			joints.position = [0,-1.6,2.5,0,-1,0,0]
			joints.velocity = [0,0,0,0,0,0,0]
			joints.effort = [0,0,0,0,0,0,0]
			pub_Joints.publish(joints)
			print(' Arm init.')
			n = n + 1
		# while n < 10:
		# 	pose[4] = pose[4] + 0.1
		# 	joints.header = Header()
		# 	joints.header.stamp = rospy.Time.now()
		# 	joints.position = pose
		# 	pub_Joints.publish(joints)
		# 	n = n+1
		rate.sleep()


if __name__ == '__main__':
  try:
    sim_real_arm()
    # rospy.on_shutdown(turn_off)
  except rospy.ROSInterruptException:
    pass

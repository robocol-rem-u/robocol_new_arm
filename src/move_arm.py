#!/usr/bin/env python3
import sys
import copy
import rospy
import moveit_commander 
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
#from moveit_commander.conversions import pose_to_list

def principal():
    rospy.init_node('move_arm')
    rate = rospy.Rate(10) # 10hz
    moveit_commander.roscpp_initialize(sys.argv)
    robot = moveit_commander.RobotCommander()
    # We can get the joint values from the group and adjust some of the values:
    joint_goal = move_group.get_current_joint_values()
    joint_goal[0] = 0
    joint_goal[1] = -pi/4
    joint_goal[2] = 0
    joint_goal[3] = -pi/2
    joint_goal[4] = 0
    joint_goal[5] = pi/3
    # The go command can be called with joint values, poses, or without any
    # parameters if you have already set the pose or joint target for the group
    move_group.go(joint_goal, wait=True)
    # Calling ``stop()`` ensures that there is no residual movement
    move_group.stop()
    while not rospy.is_shutdown():
      print('while')
      rate.sleep()


if __name__ == '__main__':
    try:
        principal()
    except rospy.ROSInterruptException:
        pass
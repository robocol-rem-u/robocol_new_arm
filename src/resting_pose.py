#!/usr/bin/env python
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import rospy

j0 = 0.0
j1 = 0.0
j2 = 0.0
j3 = 0.0
j4 = 0.0
j5 = 0.0
j6 = 0.0
v0 = 0.1
v1 = 0.1
v2 = 0.1
v3 = 0.1
v4 = 0.1
v5 = 0.1
v6 = 0.1

def changeDir(j,v,n):
    if j>n:
        print('if')
        v = -0.1
    elif j<-n:
        print('elif')
        v = 0.1
    else:
        v = v
    return v

def moving_test():
    j1 = round(j1+v1,1)
    j2 = round(j2+v2,1)
    j3 = round(j3+v3,1)
    j4 = round(j4+v4,1)
    j5 = round(j5+v5,1)
    j6 = round(j6+v6,1)
    v1 = changeDir(j1,v1,2)
    v2 = changeDir(j2,v2,1.5)
    v3 = changeDir(j3,v3,1.5)
    v4 = changeDir(j4,v4,2.5)
    v5 = changeDir(j5,v5,1.5)
    v6 = changeDir(j6,v6,3)

def move_arm():
    global j0,j1,j2,j3,j4,j5,j6
    global v0,v1,v2,v3,v4,v5,v6
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('joint_state_publisher')
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
      hello_str = JointState()
      hello_str.header = Header()
      hello_str.header.stamp = rospy.Time.now()
      hello_str.name = ['robocol_joint1','robocol_joint2','robocol_joint3','robocol_joint4','robocol_joint5','robocol_joint6']
      hello_str.position = [j1,j2,j3,j4,j5,j6]
      hello_str.velocity = []
      hello_str.effort = []
      hello_str.header.stamp = rospy.Time.now()
      pub.publish(hello_str)
      
      rate.sleep()


if __name__ == '__main__':
    try:
        move_arm()
    except rospy.ROSInterruptException:
        pass

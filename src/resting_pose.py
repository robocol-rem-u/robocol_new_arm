#!/usr/bin/env python
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from master_msgs.msg import traction_Orders, connection, arm_Orders, rpm, current,pots,sensibility
import rospy

j0 = 0.0
j1 = 0.0
j2 = 0.0
j3 = 0.0
j4 = 2.0
j5 = 0.0
j6 = 0.0
v0 = 0.1
v1 = 0.1
v2 = 0.1
v3 = 0.1
v4 = 0.1
v5 = 0.1
v6 = 0.1

pots_present = pots()
actual_J0 = 0.0
actual_J1 = 0.0
actual_J2 = 0.0
actual_J3 = 0.0
actual_J4 = 0.0
actual_J5 = 0.0

pasado_J0 = 0.0
pasado_J1 = 0.0
pasado_J2 = 0.0
pasado_J3 = 0.0
pasado_J4 = 0.0
pasado_J5 = 0.0

#d = 

def pots_Callback(param):
    global pots_present
    global actual_J0,actual_J1,actual_J2,actual_J3,actual_J4,actual_J5
    print("1111")
    pots_present=param.J0
    actual_J0 = param.J0
    actual_J1 = param.J1
    actual_J2 = param.J2
    actual_J3 = param.J3
    actual_J4 = param.J4
    actual_J5 = param.J5

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
    global pots_present
    global actual_J0,actual_J1,actual_J2,actual_J3,actual_J4,actual_J5
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    
    rospy.Subscriber ('topic_pots', pots, pots_Callback)
    
    rospy.init_node('joint_state_publisher')
    rate = rospy.Rate(10) # 10hz
    print("Empezó")
    while not rospy.is_shutdown():
      hello_str = JointState()
      hello_str.header = Header()
      hello_str.header.stamp = rospy.Time.now()
      hello_str.name = ['robocol_joint1','robocol_joint2','robocol_joint3','robocol_joint4','robocol_joint5','robocol_joint6']
      #hello_str.position = [j1,j2,j3,j4,j5,j6]
      actual_J0 = -0.2436*actual_J0+834.71
      actual_J1 =  0.5*actual_J1-1735
      actual_J2 = -0.3862*actual_J2+880.6866
      actual_J3 =  -0.3585*actual_J3+709.9601
      actual_J4 =  -0.3629*actual_J4+802.7419
      actual_J5 =  0.3719*actual_J5-873.97
      actual_J0 = round((actual_J0*(3.1416))/180,4)
      actual_J1 = round((actual_J1*(3.1416))/180,4)
      actual_J2 = round((actual_J2*(3.1416))/180,4)
      actual_J3 = round((actual_J3*(3.1416))/180,4)
      actual_J4 = round((actual_J4*(3.1416))/180,4)
      actual_J5 = round((actual_J5*(3.1416))/180,4)
      print('J0: ',actual_J0)
      print('J1: ',actual_J1)
      print('J2: ',actual_J2)
      print('J3: ',actual_J3)
      print('J4: ',actual_J4)
      print('J5: ',actual_J5)
      print(' ')
      #hello_str.position = [actual_J0,actual_J1,actual_J2,actual_J3,2,actual_J5]
      hello_str.position = [actual_J0,actual_J1,actual_J2,actual_J3,actual_J4,actual_J5]
      #hello_str.position = [actual_J0,actual_J1,actual_J2,actual_J3,j4,actual_J5]
      hello_str.velocity = [0,0,0,0,0,0]
      hello_str.effort = [0,0,0,0,0,0]
      hello_str.header.stamp = rospy.Time.now()
      pub.publish(hello_str)
      rate.sleep()


if __name__ == '__main__':
    try:
        move_arm()
    except rospy.ROSInterruptException:
        pass

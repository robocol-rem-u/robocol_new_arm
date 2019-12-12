#!/usr/bin/env python3
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from master_msgs.msg import traction_Orders, connection, arm_Orders, rpm, current,pots,sensibility
import rospy

pots_present = pots()
actual_J0 = 0.0
actual_J1 = 0.0
actual_J2 = 0.0
actual_J3 = 0.0
actual_J4 = 0.0
actual_J5 = 0.0

pasados_J0 = 0.0
pasados_J1 = 0.0
pasados_J2 = 0.0
pasados_J3 = 0.0
pasados_J4 = 0.0
pasados_J5 = 0.0

iw = 0
ven = 10
#d = 

def regr(x1,y1,x2,y2):
  m = (y2-y1)/(x2-x1)
  b = y2-(m*x2)
  return m,b

def pots_Callback(param):
    global pots_present
    global iw,ven
    global actual_J0,actual_J1,actual_J2,actual_J3,actual_J4,actual_J5
    global pasados_J0,pasados_J1,pasados_J2,pasados_J3,pasados_J4,pasados_J5
    #pots_present=param.J0
    pasados_J0 += param.J0
    pasados_J1 += param.J1
    pasados_J2 += param.J2
    pasados_J3 += param.J3
    pasados_J4 += param.J4
    pasados_J5 += param.J5
    iw += 1
    if iw == ven:
      actual_J0 = pasados_J0/ven
      actual_J1 = pasados_J1/ven
      actual_J2 = pasados_J2/ven
      actual_J3 = pasados_J3/ven
      actual_J4 = pasados_J4/ven
      actual_J5 = pasados_J5/ven
      
      m0,b0 = regr(3369,0,3755,90)
      actual_J0 = m0*actual_J0+b0
      m1,b1 = regr(3210,0,2997,-90)
      actual_J1 =  (m1*actual_J1)+b1+50
      m2,b2 = regr(2254,0,2019,90)
      actual_J2 = (m2*actual_J2)+b2
      m3,b3 = regr(2008,0,2250,-90)
      actual_J3 =  m3*actual_J3+b3
      m4,b4 = regr(2188,0,2430,-90)
      actual_J4 =  (m4*actual_J4)+b4
      m5,b5 = regr(2640,90,2369,0)
      actual_J5 =  (m5*actual_J5)+b5
      

      actual_J0 = round(((actual_J0*(3.1416))/180)-1.57,4)
      actual_J1 = round((actual_J1*(3.1416))/180,4)
      actual_J2 = round((actual_J2*(3.1416))/180,4)
      actual_J3 = round(((actual_J3*(3.1416))/180)-3.1416,4)
      actual_J4 = round(((actual_J4*(3.1416))/180),4)
      actual_J5 = round((actual_J5*(3.1416))/180,4)
      pasados_J0 = 0.0
      pasados_J1 = 0.0
      pasados_J2 = 0.0
      pasados_J3 = 0.0
      pasados_J4 = 0.0
      pasados_J5 = 0.0
      iw = 0
    # print('pas0:',pasados_J0)


def move_arm():
    global pots_present
    global actual_J0,actual_J1,actual_J2,actual_J3,actual_J4,actual_J5
    rospy.init_node('joint_state_publisher')
    rospy.Subscriber ('topic_pots',pots,pots_Callback)
    pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rate = rospy.Rate(100) # 10hz
    # print("Empezó")
    while not rospy.is_shutdown():
      hello_str = JointState()
      hello_str.header = Header()
      hello_str.header.stamp = rospy.Time.now()
      hello_str.name = ['robocol_joint1','robocol_joint2','robocol_joint3','robocol_joint4','robocol_joint5','robocol_joint6']
      #hello_str.position = [j1,j2,j3,j4,j5,j6]
      
      # print('J0: ',actual_J0)
      # print('J1: ',actual_J1)
      # print('J2: ',actual_J2)
      # print('J3: ',actual_J3)
      # print('J4: ',actual_J4)
      # print('J5: ',actual_J5)
      # print(' ')
      hello_str.position = [-0.931,-1.57,actual_J2,actual_J3,-actual_J4,actual_J5]
      #hello_str.position = [actual_J0,-1.57,actual_J2,actual_J3,actual_J4,actual_J5]
      #hello_str.position = [0.0,1.57,0.0,0.0,0.0,0.0]
      #hello_str.position = [actual_J0,actual_J1,actual_J2,actual_J3,j4,actual_J5]
      hello_str.velocity = [0,0,0,0,0,0]
      hello_str.effort = [0,0,0,0,0,0]
      # hello_str.header.stamp = rospy.Time.now()
      pub.publish(hello_str)
      rate.sleep()

if __name__ == '__main__':
    try:
        move_arm()
    except rospy.ROSInterruptException:
        pass

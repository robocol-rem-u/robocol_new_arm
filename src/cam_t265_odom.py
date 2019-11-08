#!/usr/bin/env python
# from sensor_msgs.msg import JointState
# from std_msgs.msg import Header
#from realsense-ros import 
import sys
import rospy
import moveit_commander
from pprint import pprint
from nav_msgs.msg import Odometry
import matplotlib.pyplot as plt
import time

j=1
x,y,z = 0,0,0
vx,vy,vz,vt = [],[],[],[]
xmax,ymax,zmax = 0,0,0
xmin,ymin,zmin = 0,0,0
t = 0
tm = 10
pose = Odometry()

def camera_Callback(param):
    global pose
    pose = param.pose

def axesCalc():
    global xmax,ymax,zmax
    global xmin,ymin,zmin
    global x,y,z
    if(x>xmax):
      xmax = x
    if(y>ymax):
      ymax = y
    if(z>zmax):
      zmax = z
    if(x<xmin):
      xmin = x
    if(y<ymin):
      ymin = y
    if(z<zmin):
      zmin = z

def plot(axs):
  global vx,vy,vz,vt
  axs[0].plot(vt,vx,c='r')
  axs[1].plot(vt,vy,c='g')
  axs[2].plot(vt,vz,c='b')

def timeAxisCalc():
  global t,tm
  if(t>10):
    tm = 50
  if(t>50):
    tm = 100
  if(t>100):
    tm = 1000

def noiseCancel():
  global x,y,z
  noise = 0.1
  if abs(x)<noise:
    x = 0
  if abs(y)<noise:
    y = 0
  if abs(z)<noise:
    z = 0

def capture_cam():
    global j,pose
    global x,y,z,t
    global t,tm
    global xmax,ymax,zmax
    global xmin,ymin,zmin
    global vx,vy,vz,vt
    # pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('cam_odom_arm')
    rate = rospy.Rate(100) # 100hz
    rospy.Subscriber ('/camera/odom/sample',Odometry,camera_Callback)
    st = time.time()
    fig,axs = plt.subplots(3)
    fig.show()
    while not rospy.is_shutdown():
      try:
        x = round(pose.pose.position.x,2)
        y = round(pose.pose.position.y,2)
        z = round(pose.pose.position.z,2)
        print('x:',x,'y:',y,'z:',z)
        axesCalc()
        #noiseCancel()
      except:
        pass
      vx.append(x)
      vy.append(y)
      vz.append(z)
      vt.append(t)
      plot(axs)
      # axs[0].scatter(t,x,s=0.5,c='r')
      # axs[1].scatter(t,y,s=0.5,c='g')
      # axs[2].scatter(t,z,s=0.5,c='b')
      plt.pause(0.0001)
      t = time.time()-st
      #print(t)
      timeAxisCalc()
      axs[0].axis([0,tm,xmin-0.1,xmax+0.1])
      axs[1].axis([0,tm,ymin-0.1,ymax+0.1])
      axs[2].axis([0,tm,zmin-0.1,zmax+0.1])
      # hello_str = JointState()
      # hello_str.header = Header()
      # hello_str.header.stamp = rospy.Time.now()
      # hello_str.name = ['robocol_joint1','robocol_joint2','robocol_joint3','robocol_joint4','robocol_joint5','robocol_joint6']
      # hello_str.position = [j1,j2,j3,j4,j5,j6]
      # hello_str.velocity = []
      # hello_str.effort = []
      # hello_str.header.stamp = rospy.Time.now()
      # pub.publish(hello_str)
      rate.sleep()

if __name__ == '__main__':
    try:
        capture_cam()
    except rospy.ROSInterruptException:
        pass

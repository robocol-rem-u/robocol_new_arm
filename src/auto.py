#!/usr/bin/env python
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from master_msgs.msg import traction_Orders, connection, arm_Orders, rpm, current,pots,sensibility
from moveit_msgs.msg import DisplayTrajectory
from moveit_msgs.msg import RobotTrajectory
import rospy

joints = JointState()
trajectory = DisplayTrajectory()
robotTraj = RobotTrajectory()
actual_J0 = 0.0
actual_J1 = 0.0
actual_J2 = 0.0
actual_J3 = 0.0
actual_J4 = 0.0
actual_J5 = 0.0

njoints = 6
redon = 3

M4 = 'F'
M5 = 'D'

traj = []

def trajectory_Callback(param):
  global trajectory,robotTraj,traj
  global redon,njoints
  vec = param.trajectory[0].joint_trajectory.points
  for i in range(len(vec)):
    p = []
    for j in range(njoints):
      p.append(round(vec[i].positions[j],2))
    traj.append(p)

def joints_Callback(param):
    global joints
    global redon,njoints
    joints = param.position

def error_traj(a):
    global joints,traj,error,njoints
    global redon,njoints
    error = [0.0,0.0,0.0,0.0,0.0,0.0]
    try:
      for i in range(njoints):
         error[i] = round(traj[a][i]-joints[i],2)
    except:
      print("No trajectory or actual joints.")
    return error

def print_info():
  try:
    print("Trayectoria:")
    print(traj[0])
    print("Joints:")
    print(joints)
    print("Error:")
    print(error_traj(0))
  except:
    pass

def auto_arm():
    global joints,traj,g
    global actual_J0,actual_J1,actual_J2,actual_J3,actual_J4,actual_J5
    #pub = rospy.Publisher('joint_states', JointState, queue_size=10)
    rospy.init_node('auto')
    rospy.Subscriber('joint_states',JointState,joints_Callback)
    rospy.Subscriber('/move_group/display_planned_path',DisplayTrajectory,trajectory_Callback)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
      print_info
      
        
      
      rate.sleep()

if __name__ == '__main__':
    try:
        auto_arm()
    except rospy.ROSInterruptException:
        pass

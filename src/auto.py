#!/usr/bin/env python
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from master_msgs.msg import traction_Orders,connection,arm_Orders,pots
from moveit_msgs.msg import DisplayTrajectory
#from moveit_msgs.msg import RobotTrajectory
from moveit_msgs.msg import MoveGroupActionFeedback

joints = JointState()
trajectory = DisplayTrajectory()
fd = MoveGroupActionFeedback()

njoints = 6
redon = 3
mot = ['B','C','D','E','F','G']
sep_pos = '#'
sep_neg = '!'
traj = []
cambio = 0


# -------------------------------------------------------------
# --------------------- CALLBACKS -----------------------------
# -------------------------------------------------------------
# Move Group Trajectory Callback.
def trajectory_Callback(param):
  global trajectory,robotTraj,traj
  global redon,njoints
  traj = []
  print('')
  print('Cargando trayectoria...')
  vec = param.trajectory[0].joint_trajectory.points
  for i in range(len(vec)):
    p = []
    for j in range(njoints):
      p.append(round(vec[i].positions[j],2))
    traj.append(p)
  print('Trayectoria:')
  print(traj)
  print('Trayectoria Almacenada.')
  # if not traj:
# Joints State Callback.
def joints_Callback(param):
  global joints
  global redon,njoints
  joints = param.position
# Move Group Feedback Callback.
def feedback_Callback(param):
  global fd
  fd = param.feedback.state
  # print(fd)
# -------------------------------------------------------------
# ---------------------- ARM CONTROL --------------------------
# -------------------------------------------------------------
def error_traj(a):
  global joints,traj,njoints
  global redon,njoints
  error = [0.0,0.0,0.0,0.0,0.0,0.0]
  try:
    for i in range(njoints):
       error[i] = round(traj[a][i]-joints[i],2)
  except:
    print("No trajectory or actual joints.")
    error = [0.0,0.0,0.0,0.0,0.0,0.0]
  return error

def move_joints(error):
  global njoints
  j = [0,0,0,0,0,0]
  for i in range(njoints):
    if error[i]>0:
      j[i] = 1
    elif error[i]<0:
      j[i] = -1
  return j

def msg(j):
  global njoints
  global sep_pos,sep_neg
  global mot
  v = [10,10,10,10,10,10]
  r = ''
  for i in range(njoints):
    r += mot[i]
    if j[i] == 1:
      r += str(v[i]) + sep_pos
    elif j[i] == -1:
      r += str(v[i]) + sep_neg
    else:
      r += '0' + sep_pos
  return r

def print_info(i):
  try:
    print("Trayectoria:")
    print(traj[i])
    print("Joints:")
    print(joints)
    print("Error:")
    print(error_traj(i))
  except:
    pass

def execTraj(i):
  global traj
  print('')
  print_info(i)
  print('*-------------------------*')
  print(" Ejecutando trayectoria...")
  print('*-------------------------*')
  print('Calculando error...')
  e = error_traj(i)
  print("Error calculado.")
  print("Calculando movimiento de juntas...")
  j = move_joints(e)
  print("Movimientos calculados.")
  print("Creando mensaje...")
  m = msg(j)
  print("Mensaje creado.")
  print('Mensaje:')
  print(m)
  print('Terminó')
  return m

# -------------------------------------------------------------
# -------------------- MAIN ROS DEF ---------------------------
# -------------------------------------------------------------
def auto_arm():
  global joints,traj
  global fd
  global arm_msg
  rospy.init_node('auto')
  rospy.Subscriber('joint_states',JointState,joints_Callback)
  rospy.Subscriber('/move_group/feedback',MoveGroupActionFeedback,feedback_Callback)
  rospy.Subscriber('/move_group/display_planned_path',DisplayTrajectory,trajectory_Callback)
  pub_Arm_Orders = rospy.Publisher('topic_arm_orders',arm_Orders, queue_size=10)
  rate = rospy.Rate(10) # 10hz
  a = 0
  while not rospy.is_shutdown():
    msg = execTraj(0)
    if msg == "B0#C0#D0#E0#F0#G0#" and a < 2:
      arm_msg = arm_Orders()
      arm_msg.header = Header()
      arm_msg.message = msg
      a += 1
      pub_Arm_Orders.publish(arm_msg)
    
    # if fd == "PLANNING":
    #   print('')
    #   print("Trayectoria:")
    #   print(traj)
    #  print('1')
    #print(fd)
    # if cambio:
    #   try:
    #     execTraj(1)
    #   except:
    #     print("ERROR.")
      # print_info()
    rate.sleep()

if __name__ == '__main__':
  try:
    auto_arm()
  except rospy.ROSInterruptException:
    pass

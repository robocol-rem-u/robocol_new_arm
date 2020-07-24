#!/usr/bin/env python3
import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import JointState
from master_msgs.msg import traction_Orders,connection,arm_Orders,pots,arm_auto_status
from moveit_msgs.msg import DisplayTrajectory
#from moveit_msgs.msg import RobotTrajectory
from moveit_msgs.msg import MoveGroupActionFeedback
import threading,time

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
cumple = [0,0,0,0,0,0]
exe,stop,end,sd,tc = 0,0,0,0,1
# -------------------------------------------------------------
# ----------------------- THREADS -----------------------------
# -------------------------------------------------------------
def thread_joint_arrive():
  global cumple
  for i in range(0,6):
    if cumple[i] == 1:
      pass

def thread_comm():
  global stop,end,sd,tc,exe
  while tc==1:
    msg = input('Which action to take?')
    if msg =='e' or msg == 'E':
      print('Executing trajectory...')
      exe = 1
    if msg == 's' or msg == 'S':
      stop = 1
      print('Stopping motors...')
    if msg == 'c' or msg == 'C':
      print('Continue running...')
      stop = 0
    if msg == 'q' or msg == 'Q':
      print('Quitting...')
      stop = 1
      sd = 1
      tc = 0

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
def arm_status_Callback(param):
  global exe,stop,sd,tc
  if param.message == "Execute":
    exe = 1
  if param.message == "Stop":
    stop = 1
    exe = 0
  if param.message == 'Quit':
    stop = 1
    sd = 1
    tc = 0


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
    # if i == 3:
    #   if error[i]>0:
    #     j[i] = -1
    #   elif error[i]<0:
    #     j[i] = 1
    # else:
    if error[i]>0:
      j[i] = 1
    elif error[i]<0:
      j[i] = -1
  return j

def msg(j):
  global njoints
  global sep_pos,sep_neg
  global mot
  global cumple
  vmax = 20
  v = [vmax,vmax,40,30,30,40]
  r = ''
  for i in range(njoints):
    r += mot[i]
    if cumple[i] == 1:
      r += '0' + sep_pos
    elif j[i] == 1:
      if i == 4:
        r += str(v[i]) + sep_neg
      else:
        r += str(v[i]) + sep_pos
    elif j[i] == -1:
      if i == 4:
        r += str(v[i]) + sep_pos
      else:
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
  # print('')
  # print_info(i)
  # print('*-------------------------*')
  # print(" Ejecutando trayectoria...")
  # print('*-------------------------*')
  # print('Calculando error...')
  e = error_traj(i)
  # print("Error calculado.")
  # print("Calculando movimiento de juntas...")
  j = move_joints(e)
  # print("Movimientos calculados.")
  # print("Creando mensaje...")
  m = msg(j)
  # print("Mensaje creado.")
  # print('Mensaje:')
  # print(m)
  # print('Termino')
  return m

def comprobar(t):
  global joints,njoints
  global cumple,exe,stop
  r = 0.1
  a = t
  j = 0
  print('')
  print('')
  print('')
  print('TESTING CONDITIONS...')
  print('Trajectory #:',str(t))
  for i in range(0,6):
    if i == 0 or i == 1:
      cumple[i] = 1
      j += 1
    else:
      print('JOINT:',str(i+1))
      print('Present:',joints[i])
      print('Requested:',traj[t][i])
      if joints[i] > traj[t][i]-r and joints[i] < traj[t][i]+r:
        print('Joint',str(i+1),'arrived.')
        j = j+1
        cumple[i] = 1
      else:
        print("JOINT",str(i+1),"HAS NOT ARRIVED.")
        cumple[i] = 0
  if j == 6:
    a = t+1
    print('Next trajectory.')
    #stop = 1
    cumple = [0,0,0,0,0,0]
    #exe = 0
  return a

def turn_off():
  global tc
  tc = 0
  print('Node is shutting down...')
  print('ALL MOTORS TO 0')
  # reason = 'User ask to close.'
  # rospy.signal_shutdown(reason)

# -------------------------------------------------------------
# -------------------- MAIN ROS DEF ---------------------------
# -------------------------------------------------------------
def auto_arm():
  global joints,traj
  global fd,sd,stop,exe
  global arm_msg
  x = threading.Thread(target=thread_joint_arrive)
  x.start()
  y = threading.Thread(target=thread_comm)
  y.start()
  rospy.init_node('auto')
  rospy.Subscriber('joint_states',JointState,joints_Callback)
  rospy.Subscriber('topic_arm_status',arm_auto_status,arm_status_Callback)
  rospy.Subscriber('/move_group/feedback',MoveGroupActionFeedback,feedback_Callback)
  rospy.Subscriber('/move_group/display_planned_path',DisplayTrajectory,trajectory_Callback)
  # --- PUBLISHERS --- #
  pub_Arm_Orders = rospy.Publisher('topic_arm_orders',arm_Orders,queue_size=10)
  pub_Arm_Status = rospy.Publisher('topic_arm_status',arm_auto_status,queue_size=10)
  rate = rospy.Rate(20) # 10hz
  a = 0
  t = 0
  while not rospy.is_shutdown():
    msg = ''
    arm_msg = arm_Orders()
    arm_msg.header = Header()
    # print(y.isAlive())
    # st = arm_auto_status()
    # st.header = Header()
    # st.message = 'Test'
    # pub_Arm_Status.publish(st)
    if exe:
      try:
        traj[0]
        t = comprobar(t)
        msg = execTraj(t)
      except Exception as e:
        print('')
        print('No trajectory.')
        exe = 0
        t = 0
      arm_msg.message = msg
      pub_Arm_Orders.publish(arm_msg)
    
    if stop == 1:
      msg = 'B0#C0#D0#E0#F0#G0#'
      arm_msg.message = msg
      pub_Arm_Orders.publish(arm_msg)
      exe = 0
      stop = 0
      t = 0
    if sd:
      reason = 'User ask to close.'
      rospy.signal_shutdown(reason)
    rate.sleep()
  tc = 0
  # stop_threads = False
  # t1 = threading.Thread(target = thread_comm)
  # t1.start() 
  # time.sleep(1) 
  # stop_threads = True
  # t1.join() 

if __name__ == '__main__':
  try:
    auto_arm()
    rospy.on_shutdown(turn_off)
  except rospy.ROSInterruptException:
    print("Killed...")
    end = 1
    pass

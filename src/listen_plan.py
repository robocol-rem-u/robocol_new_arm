#!/usr/bin/env python
from master_msgs.msg import arm_Orders
import rospy

def prueba():
    rospy.init_node('nodo_prueba_brazo', anonymous=True)
    pub_Arm_Orders = rospy.Publisher('topic_arm_orders',arm_Orders,queue_size=10)
    msg = arm_Orders()
    rate = rospy.Rate(1)
    print('inicio')
    while not rospy.is_shutdown():
        pub_Arm_Orders.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        prueba()
    except rospy.ROSInterruptException:
        pass
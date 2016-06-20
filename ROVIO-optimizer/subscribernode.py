#!/usr/bin/env python
import rospy
import math

from nav_msgs.msg import Odometry


def odometryCb(msg):
    #print msg.pose.pose
    global zwpose
    zwpose=msg.pose.pose
   

if __name__ == "__main__":
    rospy.init_node('oodometry', anonymous=True) #make node 
    savepose=rospy.Subscriber('rovio/odometry',Odometry,odometryCb)
    rospy.spin()
print("Last Pose")
pose_x =zwpose.position.x
pose_y =zwpose.position.y
pose_z =zwpose.position.z
error=pose_x*pose_x+pose_y*pose_y+pose_z*pose_z
print ("Beginn of Position login")
print pose_x
print pose_y
print pose_z
print error


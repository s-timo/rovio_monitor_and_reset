#!/usr/bin/env python
import rospy
import math

from nav_msgs.msg import Odometry

#to be used in connection with roptimzer
#return the last pose ROVIO publish on the ROS Network, return as soon as the programm is closed

def odometryCb(msg): #saving the last position
    #print msg.pose.pose
    global zwpose
    zwpose=msg.pose.pose
   

if __name__ == "__main__":
    rospy.init_node('oodometry', anonymous=True) #prepare node 
    savepose=rospy.Subscriber('rovio/odometry',Odometry,odometryCb)
    rospy.spin()
print("Last Pose")
pose_x =zwpose.position.x #print last position
pose_y =zwpose.position.y
pose_z =zwpose.position.z
error=pose_x*pose_x+pose_y*pose_y+pose_z*pose_z
if error >10:
	error=10 #Level of the error
print ("Beginn of Position login")
print pose_x
print pose_y
print pose_z
print error


#!/usr/bin/env python
import rospy
import math

from nav_msgs.msg import Odometry

from rospy_tutorials.srv import *

global lastdelta
global maxspeed
global initialoffset
global offset
global delay
global i
global hysterese
global Empty


def odometryCb(msg):
    #print msg.pose.pose
   	#time=rospy.Time.now()
 	#print rospy.Time.now()-time
	global lastdelta
 	global zwpose
 	global maxspeed
 	global initialoffset
 	global delay
 	global i
 	global hysterese
 	global offset


 	if i<21:
 		initialoffset[i]= rospy.get_time()-msg.header.stamp.to_sec()
 		i=i+1
 		if i==20:
 			initialoffset.sort()
 			offset=initialoffset[10]
 			lastdelta=rospy.get_time()-msg.header.stamp.to_sec()- offset
 	else:
	 	deltatime=rospy.get_time()-msg.header.stamp.to_sec()- offset
	 	#deltatime=msg.header.stamp.to_sec()-lastmsg-offset
	 	#vergleich= rospy.Duration(25000000)
	 	#if deltatime>24816036:
	 	#	delay=deltatime
	 	#	print delay
	 	#print deltatime
	 	#print deltatime.secs
	 	#print deltatime
	 	deriv=math.fabs( deltatime-lastdelta)
	 	#print deltatime 
	 	if deriv>0.025: #bei aktuele-header ->200000000
	 		hysterese=hysterese+1
	 		if hysterese > 4: #min 2 mal muss threshold uebertreten werden, bis Reset ausgeloest wird
	 			if deltatime>0.0:# deltatimif hysterese > 2:#min 2 mal musse muss auch bedingung erfuellen
	 				print 'Rovio reset delay'
	 	else:
	 		hysterese=0
	 	lastdelta=deltatime
	
	lastmsg=msg.header.stamp.to_sec()
	zwpose=msg.pose
	speed= math.sqrt(msg.twist.twist.linear.x*msg.twist.twist.linear.x+msg.twist.twist.linear.y*msg.twist.twist.linear.y+msg.twist.twist.linear.z*msg.twist.twist.linear.z)
	if speed>maxspeed:
	   	maxspeed=speed
	if speed> 0.4:#1.5
		reset("speed",zwpose)
   		
def reset(reason, pose):
	
	print "Rovio reseted due to: "+reason
	rospy.wait_for_service('/rovio/reset')
	rovioreset=rospy.ServiceProxy('/rovio/reset',SrvResetToPose)
	response=rovioreset(pose)
	print "Rovio reseted"


if __name__ == "__main__":

	rospy.init_node('oodometry', anonymous=True) #make node 
	global lastdelta
	global maxspeed
	global initialoffset
	global delay
	global i
	global hysterese

	initialoffset=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	hysterese=0
	i=0
	lastdelta=rospy.get_time()
	maxspeed=0
	
	delay=0
	print "Programm gestartet"
	savepose=rospy.Subscriber('rovio/odometry',Odometry,odometryCb)
	rospy.spin()
print("Max Speed")
print maxspeed



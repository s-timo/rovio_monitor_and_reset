#!/usr/bin/env python
import rospy
import math

from nav_msgs.msg import Odometry
from geometry_msgs import *

from rovio_monitor.srv import *

global lastdelta 	# last difference between header-timestamp and now array, everytime one count ahead
global maxspeed		#nice to know
global initialoffset #array to find median of offset
global offset 		#offset between Header timestamp and now
global i 			#counting variabel for save pose and initializing
global hysterese 	#security that one short lag do not reset rovio
global initalizing 	#bool for (re)initialize the monito
global zwpose 		#array of poses for save, to when rovio crashes


def odometryCb(msg):
    #print msg.pose.pose
   	#time=rospy.Time.now()
 	#print rospy.Time.now()-time
	
 	#make global variables available
	global lastdelta
 	global zwpose
 	global maxspeed
 	global initialoffset
 	global i
 	global hysterese
 	global offset
 	global initalizing

 	if initalizing:
 		initialoffset[i]= rospy.get_time()-msg.header.stamp.to_sec() #initializing the offset between Headertimestamp and now
 		if i==19:
 			initialoffset.sort()
 			offset=initialoffset[10] #median of all meassured offsets
 			lastdelta[0]=rospy.get_time()-msg.header.stamp.to_sec()- offset
 			initalizing=False
 			#print "Initalzing of Monitor finished"

 	else:
	 	deltatime=rospy.get_time()-msg.header.stamp.to_sec()- offset-lastdelta[i+1]%20 #time between header timestamp and now, upcounting corigated
	 
	 	deriv=deltatime-lastdelta[i] #time in [s] with which the delay increase

	 	
	 	print deltatime 
	 	#print deriv
	 	if deriv>0.015: # default. 0.025 trigger, if delay increase to fast
	 		hysterese=hysterese+1
	 		
	 	#elif deltatime>0.05 :# trigger, if delay is too bis muss zuerst in live probiert werden ob dort dely auch dauernd zunimmt
	 	#	hysterese=hysterese+1
	 	else:
	 		if hysterese>0:
	 			hysterese=hysterese-0.2
	 		else:
	 			hysterese=0
	 	if hysterese > 2: #min 3 mal muss Indikator anspringen bis ausgeloest wird, hysteresemethode muss angepasst werden
	 		reset("delay",zwpose[i])#reset call, with value before 20 times (1 second)
	 		hysterese=0

	 	lastdelta[(i+1)%20]=deltatime #save old delay value
		#lastmsg=msg.header.stamp.to_sec() #save old headertime. Spacing between the messages are randomly distributed, that's why this mehtode isn't in use

		#Auslesen des Aktuellen absoluten speed
		speed= msg.twist.twist.linear.x*msg.twist.twist.linear.x+msg.twist.twist.linear.y*msg.twist.twist.linear.y+msg.twist.twist.linear.z*msg.twist.twist.linear.z
	
		#nice to know
		#if speed>maxspeed:
		#  	maxspeed=speed
		if speed> 2.25:#default: 2.25=1.5 squarde. To safe computational time
			reset("speed",zwpose[i])#reset call with value before 20 times 81 second)

	#verwaltung
	zwpose[i]=msg.pose #save actual pose
		
	i=(i+1)%20 #0-19 usw.

   		
def reset(reason, pose):#Reset function reason, Pose to reset
	global initalizing

	print "Rovio reseted due to: "+reason
	rospy.wait_for_service('/rovio/reset_to_pose')
	rovioreset=rospy.ServiceProxy('/rovio/reset_to_pose',SrvResetToPose) #arm service call 

	newpose=geometry_msgs.msg.Pose()
	newpose.position=pose.pose.position
	newpose.orientation=pose.pose.orientation #make Pose without covariance ready
	response=rovioreset(newpose)#trigger servicecall 
	initalizing=True# make monitor programm initializing again
	#print "Rovio reseted, Monitor reinitializing"


if __name__ == "__main__": #entry

	rospy.init_node('oodometry', anonymous=True) #make node 
	
	#initializing the global variables
	global lastdelta
	global maxspeed
	global initialoffset
	global i
	global hysterese
	global initalizing
	global zwpose

	zwpose=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	initialoffset=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	hysterese=0
	i=0
	lastdelta=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
	maxspeed=0
	initalizing=True


	print "Monitor V4.8 started"
	#rovio listener defining/start
	savepose=rospy.Subscriber('rovio/odometry',Odometry,odometryCb)
	rospy.spin()

#print("Max Speed")
#print maxspeed
print 'Monitor finished cleanly'
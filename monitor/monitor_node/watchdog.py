#!/usr/bin/env python
import rospy
import math

from nav_msgs.msg import Odometry
from geometry_msgs import *

from rovio_monitor.srv import *

global lastdelta 	# last difference between header-timestamp and now
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
	
 	#globale Variabeln verfuegbar mache
	global lastdelta
 	global zwpose
 	global maxspeed
 	global initialoffset
 	global i
 	global hysterese
 	global offset
 	global initalizing

 	if initalizing:
 		initialoffset[i]= rospy.get_time()-msg.header.stamp.to_sec() #initialisierung des offset zwischen Headertimestamp und aktuel
 		if i==19:
 			initialoffset.sort()
 			offset=initialoffset[10] #Median aller gemessenen Offfsets
 			lastdelta=rospy.get_time()-msg.header.stamp.to_sec()- offset
 			initalizing=False
 			#print "Initalzing of Monitor finished"

 	else:
	 	deltatime=rospy.get_time()-msg.header.stamp.to_sec()- offset #Zeit zwischen aktueller zeit und header Timestamp
	 
	 	deriv=deltatime-lastdelta #Zeit in s mit der der Delay ansteigt
	 	
	 	print deltatime 
	 	#print deriv
	 	if deriv>0.015: # default. 0.025 ausloeseargument, wenn delay zu schnell steigt
	 		hysterese=hysterese+1
	 		
	 	#elif deltatime>0.05 :# ausloeseargument, wenn delay zu gross ist, muss zuerst in live probiert werden ob dort dely auch dauernd zunimmt
	 	#	hysterese=hysterese+1
	 	else:
	 		if hysterese>0:
	 			hysterese=hysterese-0.2
	 		else:
	 			hysterese=0
	 	if hysterese > 2: #min 3 mal muss Indikator anspringen bis ausgeloest wird, hysteresemethode muss angepasst werden
	 		reset("delay",zwpose[i])#reset Aufruf, mit Wert von vor 20 mal
	 		hysterese=0

	 	lastdelta=deltatime #alte Delaytime global speichern
		#lastmsg=msg.header.stamp.to_sec() #alte Headertime speichern. Abstand zwischen Msgs sind aber randowm daher nicht in gebrauch

		#Auslesen des Aktuellen absoluten speed
		speed= msg.twist.twist.linear.x*msg.twist.twist.linear.x+msg.twist.twist.linear.y*msg.twist.twist.linear.y+msg.twist.twist.linear.z*msg.twist.twist.linear.z
	
		#nice to know
		#if speed>maxspeed:
		#  	maxspeed=speed
		if speed> 2.25:#default: 2.25=1.5 im Qudrat um Comptime zu sparen (Wurzelziehen)
			reset("speed",zwpose[i])#reset Aufruf, mit Wert von vor 20 mal

	#verwaltung
	zwpose[i]=msg.pose #aktuelle Pose in Array schreiben
		
	i=(i+1)%20 #0-19 usw.

   		
def reset(reason, pose):#Reset funktion Grund, Pose to reset
	global initalizing

	print "Rovio reseted due to: "+reason
	rospy.wait_for_service('/rovio/reset_to_pose')
	rovioreset=rospy.ServiceProxy('/rovio/reset_to_pose',SrvResetToPose) #service call bereit machen

	newpose=geometry_msgs.msg.Pose()
	newpose.position=pose.pose.position
	newpose.orientation=pose.pose.orientation #Pose ohne covariance bereitstellen
	response=rovioreset(newpose)#Servicecall ausloesen
	initalizing=True# Monitor-Programm wieder zum initialisieren bringen
	#print "Rovio reseted, Monitor reinitializing"


if __name__ == "__main__": #Einstiegspunkt

	rospy.init_node('oodometry', anonymous=True) #make node 
	
	#initialisieren der globalen Variablen
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
	lastdelta=0
	maxspeed=0
	initalizing=True


	print "Monitor V4.8 started"
	#rovio listener definieren/laufen lassen
	savepose=rospy.Subscriber('rovio/odometry',Odometry,odometryCb)
	rospy.spin()

#print("Max Speed")
#print maxspeed
print 'Monitor finished cleanly'
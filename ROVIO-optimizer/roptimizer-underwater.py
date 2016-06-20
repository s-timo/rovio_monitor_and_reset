import os
import subprocess
import pexpect
import time

naming=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
naming[0]="pos_0 "
naming[1]="pos_1 "
naming[2]="pos_2 "
naming[3]="vel_0 "
naming[4]="vel_1 "
naming[5]="vel_2 "
naming[6]="acb_0 "
naming[7]="acb_1 "
naming[8]="acb_2 "
naming[9]="gyb_0 "
naming[10]="gyb_1 "
naming[11]="gyb_2 "
naming[12]="vep "
naming[13]="att_0 "
naming[14]="att_1 "
naming[15]="att_2 "
naming[16]="vea "
naming[17]="dep "
naming[18h]="nor "

bestvalues=[0.001,0.001,0.001,0.0004,0.0004,0.0004,0.0000001,0.0000001,0.0000001,0.0000038,0.0000038,0.0000038,0.0000001,0.000076,0.000076,0.000076,0.00001, 0.0001,0.00001]
changingvalues=[0.01,0.01,0.01,0.001,0.001,0.001,0.000001,0.000001,0.000001,0.000038,0.000038,0.000038,0.000001,0.00076,0.00076,0.00076,0.0001, 0.001,0.0004] #standard each is one magnitude bigger
it_delta=[0.0001,0.0001,0.0001,0.00001,0.00001,0.00001,0.00000001,0.00000001,0.00000001,0.0000001,0.0000001,0.0000001,0.00000001,0.000001,0.000001,0.000001,0.000001, 0.00001,0.000001]
errors=[0,1,2,3,4,5,6,7,8,9,10]
for x in range(0,19):
	 print naming[x]+repr(bestvalues[x])+" "

for iteration in range(0,6):#number of iteration
	for variab in range(0,19): #go through all variables
		for change in range(0,11):#try different configs
			changingvalues[variab]=bestvalues[variab]+(5-change)*it_delta[variab] 
			bagerror=[0,0,0,0,0]
			xpos=[0,0,0,0,0]
			ypos=[0,0,0,0,0]
			zpos=[0,0,0,0,0]
			with open('/home/scubo/catkin_ws/src/rovio/cfg/rovio_duo-o.info', 'r') as file:
			    data = file.readlines()# read in the config


			for x in range(0,18):
				 data[152+x]= naming[x]+repr(changingvalues[x])+';\n'
			#change the config	 
			# and write everything back
			with open('/home/scubo/catkin_ws/src/rovio/cfg/rovio_duo-o.info', 'w') as file:
			    file.writelines( data )
			#start rovio
			print(naming[variab]+ " wird iteriert mit Wert " +repr(changingvalues[variab]))
			for difbags in range(0,1):
				rovionode = pexpect.spawn('roslaunch /home/scubo/catkin_ws/src/rovio/launch/rovio_node_bag-o.launch',timeout= 180)
				print("Rovio startet")
			
				subscribernode =pexpect.spawn('python subscribernode.py ', timeout= 180)

				rovionode.expect('process has finished cleanly', timeout= 180)
				#print("Rovio finsished")
				rovionode.sendcontrol('c')			
				subscribernode.sendcontrol('c')#alles abschiessen
				subscribernode.expect('Beginn of Position login')

				subscribernode.readline()
				xpos[difbags]=float(subscribernode.readline())#x-pos
				ypos[difbags]=float(subscribernode.readline())#y-pos
				zpos[difbags]=float(subscribernode.readline())#z-pos
				bagerror[difbags]= float(subscribernode.readline())#error-pos
				print('x:'+repr(xpos)+" y:"+repr(ypos)+" z:"+repr(zpos)+" Error: "+ repr(bagerror[difbags]))
			errors[change]=bagerror[1]+bagerror[2]+bagerror[3]+bagerror[4]+bagerror[0]
			with open('optimlog_underwater_070616.txt', 'a') as file:
				for i in range(0,18):
					file.write(naming[i]+" "+repr(changingvalues[i])+" ")
				for i in range(1,5):
					file.write(repr(bagerror[i])+" ")
				file.write(repr(errors[change]))
				file.write('\n')
			print("logfile saved, this iteration is finished")
			
		print("Variable :"+naming[variab]+" wurde fertig iteriert")
		optimum=0

		for optfind in range(0,11):#find best iteration
			if errors[optfind]<errors[optimum]:
				optimum=optfind				
		bestvalues[variab]=bestvalues[variab]+(5-optimum)*it_delta[variab]
		changingvalues[variab]=bestvalues[variab]
		print("Bester Versuch mit Error:"+repr(errors[optimum])+" bei Versuch "+ repr(optimum)+ " mit Wert "+repr(bestvalues[variab]))
		
		
		it_delta[variab]=it_delta[variab]/10 #iterationschritte verkleinern
		if optimum==0 or optimum ==10 : #wenn optimum an rand liegt	
			print "Es muss neue Iteration auf diesem Parameter gemacht werden"
			variab=variab-1 #damit dieselbe variable wiederverwendet wird
			it_delta[variab]=it_delta[variab]*10#die iterationschrite wieder auf altenw wertt setzten









	










#script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
#rel_path = "odo.txt"
#abs_file_path = os.path.join(script_dir, rel_path)
#f = open(abs_file_path, "r")
#contents = f.readlines()

#f.close()
#print(contents)









#rovionode=pexpect.spawn('roslaunch /home/scubo/rovio_ws/src/rovio/launch/rovio_node_bag.launch')
#print('Rovio startet')
#
#print('Echo startet')

#pexpect.run('rostopic echo /rovio/odometry')


#subprocess.call('source /home/scubo/rovio_ws/devel/setup.bash ', shell=True)
#subprocess.call('roslaunch /home/scubo/rovio_ws/src/rovio/launch/rovio_node_bag.launch', shell=True)
#subprocess.call('rostopic echo /rovio/odometry', shell=True)+

#subprocess.call('rosbag play  Loop_bags/loop_1.bag', shell=True)

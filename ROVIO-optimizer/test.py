bimport math
'''
zahl = 0.00006162
magnitude=0
for x in range(0,20):
	if math.floor(zahl*math.pow(10,x))!=0:
		magnitude=x
		break
nzahl=zahl-1/math.pow(10,magnitude)
print nzahl

errors=[0,1,2,3,4,5,6,7,8,9,10]
for change in range(0,10):
	print errors[change]
'''
with open('file.txt', 'a') as file:
    file.write('input 1 \n')
print("file writen")
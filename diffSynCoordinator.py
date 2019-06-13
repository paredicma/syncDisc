################## diffSynCer ( DIFFERENT DIRECTORY CONTENT SYNCRONIZER ) ###########
#!/usr/bin/python
#-*- coding: utf-8 -*-
## Author			: Mustafa YAVUZ 
## E-mail			: msyavuz@gmail.com
## Date				: 10.06.2019
## OS System 		: Redhat/Centos 6-7, debian/Ubuntu
import os
import sys
import commands
from time import *
from string import *
##################PARAMETERS################################
writeLogFile=True
#logFile='/data/bipadmin/syncFTS/diffSynCerlogs/diffSynCer-'
logFile='logs/diffSynCoordinator-'
sshUser='admin'
stepSize=10
##################PARAMETERS################################
def get_datetime():
	my_year=str(localtime()[0])
	my_mounth=str(localtime()[1])
	my_day=str(localtime()[2])
	my_hour=str(localtime()[3])
	my_min=str(localtime()[4])
	my_sec=str(localtime()[5])	
	if(len(str(my_mounth))==1):
		my_mounth="0"+my_mounth		
	if(len(my_day)==1):
		my_day="0"+my_day
	if(len(my_hour)==1):
		my_hour="0"+my_hour
	if(len(my_min)==1):
		my_min="0"+my_min
	if(len(my_sec)==1):
		my_sec="0"+my_sec
	return my_year+"."+my_mounth+"."+my_day+" "+my_hour+":"+my_min+":"+my_sec
def fileAppendWrite(file, writeText):
	try :
		fp=open(file,'ab')
		fp.write(writeText+'\n')
		fp.close()
	except :
		print ('!!! An error is occurred while writing file !!!')
def logWrite(myLogFile,myLogText):
	if(writeLogFile):
#		print (logText)
		myLogText='* ('+get_datetime()+') '+myLogText
		fileAppendWrite(myLogFile+justToday()+'.log',myLogText)		
	else:
		print (logText)
def justToday():
	myDay=int(strftime('%d'))
	myMonth=int(strftime('%m'))
	myYear=int(strftime('%Y'))
	myDayStr=str(myDay)
	myMonthStr=str(myMonth)
	if (len(myDayStr)==1):
		myDayStr='0'+myDayStr
	if (len(myMonthStr)==1):
		myMonthStr='0'+myMonthStr
	return myDayStr+myMonthStr+str(myYear)
def main():
	if (os.path.exists("logs")==False):
		os.system("mkdir -p logs")
#	print ('Please specify range (like 10 20)')
	logWrite(logFile,'INFO  :: diffSynCoordinator was STARTED.  --> '+get_datetime())
	print('INFO  :: diffSynCoordinator was STARTED.  --> '+get_datetime())
	firstNum=int(sys.argv[1])
	lastNum=int((sys.argv[2]))
	while ((firstNum+stepSize)<=lastNum):
		os.system('nohup python diffSyncer.py '+str(firstNum)+' '+str(firstNum+stepSize-1)+' &')
		logWrite(logFile,'INFO  :: python diffSyncer.py '+str(firstNum)+' '+str(firstNum+stepSize-1)+' was started. ')
		firstNum+=stepSize
		sleep(3)
	if(firstNum<=lastNum):
		os.system('nohup python diffSyncer.py '+str(firstNum)+' '+str(lastNum)+' &')
		logWrite(logFile,'INFO  :: python diffSyncer.py '+str(firstNum)+' '+str(lastNum)+' was started. ')
	logWrite(logFile,'INFO  :: diffSynCoordinator was ENDED.  --> '+get_datetime())
	print('INFO  :: diffSynCoordinator was ENDED.  --> '+get_datetime())
main()

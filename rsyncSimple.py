################## rsyncSimple ( DIRECTORY SYNCRONIZER ) ###########
#!/usr/bin/python
#-*- coding: utf-8 -*-
## Author			: Mustafa YAVUZ 
## E-mail			: msyavuz@gmail.com
## Date				: 12.06.2019
## OS System 		: Redhat/Centos 6-7, debian/Ubuntu
import os
import commands
from time import *
from string import *
##################PARAMETERS################################
smallSizeDirList=['/data/test1/','/data/test2/','/data/test3/']
remoteServer='10.10.10.141'
writeLogFile=True
logFile='logs/rsyncSimple-'
sshUser='admin'
##################PARAMETERS################################
def lastCharChecker(dName):
	if(dName[len(dName)-1]=='/'):
		return dName
	else:
		return dName+'/'
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
def fileAppendWrite(file, writeText):
	try :
		fp=open(file,'ab')
		fp.write(writeText+'\n')
		fp.close()
	except :
		print ('!!! An error is occurred while writing file !!!')
def logWrite(logFile,logText):
	if(writeLogFile):
#		print (logText)
		logText='* ('+get_datetime()+') '+logText
		fileAppendWrite(logFile+justToday()+'.log',logText)		
	else:
		print (logText)
def makeRsync(dirName,remoteIP,remoteDir):
	logWrite(logFile,'INFO ::  makeRsync :: rsync will start for directory -> '+dirName)
	returnCmd,cmdResponse = commands.getstatusoutput("rsync -e 'ssh -q'  --bwlimit=10000   -arzP "+dirName+"  "+sshUser+"@"+remoteIP+":"+remoteDir+"")
	if (str(returnCmd)=='0'):
		logWrite(logFile,cmdResponse)
		logWrite(logFile,'INFO ::  makeRsync :: rsync was completed with successfully for directory -> '+dirName)
	else:
		logWrite(logFile,cmdResponse)
		logWrite(logFile,'!!! ERROR  ::  makeRsync :: rsync was NOT completed ( You should check the problem ) for directory -> '+dirName)
def main():
	if (os.path.exists("logs")==False):
		os.system("mkdir -p logs")	
	for  smallSizeDir in smallSizeDirList:
		makeRsync(lastCharChecker(smallSizeDir),remoteServer,lastCharChecker(smallSizeDir))
main()

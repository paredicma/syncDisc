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
localeMainDir='/data/mainDir/'
remoteServer='10.20.30.141'
remoteMainDir='/data/mainDir/'
writeLogFile=True
logFile='logs/diffSynCer-'
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
def diffFileCoppier(localFileName,remoteIP,remoteFileName):
	logWrite(logFile,'INFO :: diffFileCoppier() is starting for local file -> '+localFileName)
	scopyResult=os.system('scp -q -o "StrictHostKeyChecking no" -o "ConnectTimeout=5" '+localFileName+' '+remoteIP+':'+remoteFileName+'')
	if (str(scopyResult) == '0'):
		logWrite(logFile,'INFO :: diffFileCoppier() was fineshed for local file -> '+localFileName)
	else:
		logWrite(logFile,'!!! ERROR  ::  diffFileCoppier()  was NOT completed for file -> '+localFileName)
def diffFileDeleter(remoteIP,remoteFileName):
	logWrite(logFile,'INFO :: diffFileDeleter() is starting for remote file -> '+remoteFileName)
	removeResult=os.system('ssh -q -o "StrictHostKeyChecking no" -o "ConnectTimeout=5" '+remoteIP+' -C "rm -f '+remoteFileName+'"')	
	if (str(removeResult) == '0'):
		logWrite(logFile,'INFO :: diffFileDeleter() was fineshed for remote file -> '+remoteFileName)
	else:
		logWrite(logFile,'!!! ERROR  ::  diffFileDeleter()  was NOT completed for file -> '+remoteFileName)
def diffLister(dirName,remoteIP,remoteDir,subDir):
	logWrite(logFile,'INFO :: diffLister() will start for local directory -> '+dirName)
	returnLocalCmd = os.system('ls '+lastCharChecker(dirName)+lastCharChecker(subDir)+'* > listDir/local'+subDir+'.list')
	returnRemoteCmd = os.system('ssh -q -o "StrictHostKeyChecking no" -o "ConnectTimeout=5" '+remoteIP+' -C "ls '+lastCharChecker(remoteDir)+lastCharChecker(subDir)+'*" > listDir/remote'+subDir+'.list')
	if (str(returnLocalCmd)=='0' and str(returnRemoteCmd)=='0'):
		logWrite(logFile,'INFO ::  diffLister() :: local and remote dir list files were completed for directory -> '+subDir)
		returnCmd,returnDiffList = commands.getstatusoutput('diff listDir/local'+subDir+'.list listDir/remote'+subDir+'.list')
#		print ('result:'+ str(returnCmd))
#		print ('list :'+ str(diffList))
		diffList=returnDiffList.split('\n')
		if (str(returnCmd)=='256'):
#			if (len(diffList)>2):
			for diffFileName in diffList:
#				print ( diffFileName )
				if ( diffFileName[:2] == '< ' ):
					diffFileCoppier(diffFileName[2:],remoteIP,lastCharChecker(remoteDir)+lastCharChecker(subDir))
##					diffFileCoppier(lastCharChecker(dirName)+lastCharChecker(subDir)+diffFileName[2:],remoteIP,lastCharChecker(remoteDir)+lastCharChecker(subDir))
				elif ( diffFileName[:2] == '> ' ):
					diffFileDeleter(remoteIP,diffFileName[2:])
#						diffFileDeleter(remoteIP,lastCharChecker(remoteDir)+lastCharChecker(subDir)+diffFileName[2:])
		elif(str(returnCmd)=='0'):
			logWrite(logFile,'INFO ::  diffLister() :: There is no difference for directory -> '+subDir)
		else:
			logWrite(logFile,'!!! ERROR  ::  diffLister() :: While using "diff command" for files listDir/local'+subDir+'.list and listDir/remote'+subDir+'.list')
	else:
		logWrite(logFile,'!!! ERROR  ::  diffLister() :: diffLister was NOT completed for  directory -> '+subDir)
def main():
	if (os.path.exists("listDir")==False):
		os.system("mkdir -p listDir")
	if (os.path.exists("logs")==False):
		os.system("mkdir -p logs")
#	print ('Please specify range (like 10 20)')
	firstNum=int(sys.argv[1])
	lastNum=int((sys.argv[2]))
	while (firstNum<=lastNum):
		diffLister(localeMainDir,remoteServer,remoteMainDir,str(firstNum))
		firstNum+=1
main()

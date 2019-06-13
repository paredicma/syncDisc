################## rdsync ( Remote DIRECTORY SYNCRONIZER ) ###########
#!/usr/bin/python
#-*- coding: utf-8 -*-
## Author			: Mustafa YAVUZ 
## E-mail			: msyavuz@gmail.com
## Date				: 24.05.2019
## OS System 		: Redhat/Centos 6-7, debian/Ubuntu
import os
import commands
from time import *
from string import *
import calendar
##################PARAMETERS################################
smallSizeDirList=['/data/test1/','/data/test2/','/data/test3/']
localeMainDir='/data/mainDir/'
remoteServer='10.20.30.146'
remoteMainDir='/data/mainDir/'
writeLogFile=True
logFile='/data/admin/syncApp/logs/rdsync-'
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
def getHour():
	my_hour=str(localtime()[3])
	if(len(my_hour)==1):
		my_hour="0"+my_hour
	return my_hour
def getOneHourBefore():
	my_hourRaw=int(localtime()[3])
	if ( my_hourRaw==0 ):
		return '24'
	else:
		myOneHourBefore=str(my_hourRaw-1)
		if(len(myOneHourBefore)==1):
			myOneHourBefore="0"+myOneHourBefore
		return myOneHourBefore	
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
def oneDayBefore():
	myDay=int(strftime('%d'))-1
	myMonth=int(strftime('%m'))
	myYear=int(strftime('%Y'))
	if (strftime('%d')=='01'):
		myDay=int(calendar.mdays[int(strftime('%m'))-1])
		if(myMonth==1):
			myMonth=12
			myYear-=1
		else:
			myMonth-=1
	myDayStr=str(myDay)
	myMonthStr=str(myMonth)
	if (len(myDayStr)==1):
		myDayStr='0'+myDayStr
	if (len(myMonthStr)==1):
		myMonthStr='0'+myMonthStr
	return myDayStr+myMonthStr+str(myYear)
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
	myHour=getHour()
	myOneHourBefore=getOneHourBefore()
	myToday=justToday()
	myOneDayBefore=oneDayBefore()	
	if (os.path.exists(lastCharChecker(localeMainDir)+myToday+'/'+myHour)==False):
		os.system("mkdir -p "+lastCharChecker(localeMainDir)+myToday+'/'+myHour)
	if ( myHour != '00' ):
		makeRsync(lastCharChecker(localeMainDir)+lastCharChecker(myToday)+myHour+'/',remoteServer,lastCharChecker(remoteMainDir)+lastCharChecker(myToday)+myHour)
		makeRsync(lastCharChecker(localeMainDir)+lastCharChecker(myToday)+myOneHourBefore+'/',remoteServer,lastCharChecker(remoteMainDir)+lastCharChecker(myToday)+myOneHourBefore+'/')
	else:
		makeRsync(lastCharChecker(localeMainDir)+lastCharChecker(myToday)+myHour+'/',remoteServer,lastCharChecker(remoteMainDir)+lastCharChecker(myToday)+myHour+'/')
		makeRsync(lastCharChecker(localeMainDir)+lastCharChecker(myOneDayBefore)+'23/',remoteServer,lastCharChecker(remoteMainDir)+lastCharChecker(myOneDayBefore)+'23/')
	for  smallSizeDir in smallSizeDirList:
		makeRsync(lastCharChecker(smallSizeDir),remoteServer,lastCharChecker(smallSizeDir))
	makeRsync(lastCharChecker(localeMainDir)+lastCharChecker(myOneDayBefore)+myHour+'/',remoteServer,lastCharChecker(remoteMainDir)+lastCharChecker(myOneDayBefore)+myHour+'/')
main()

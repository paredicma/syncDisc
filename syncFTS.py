##################### syncDir ############
#!/usr/bin/python
#-*- coding: utf-8 -*-
## Author			: Mustafa YAVUZ 
## E-mail			: msyavuz@gmail.com
## Date				: 22.05.2019
## OS System 		: Redhat/Centos 6-7, debian/Ubuntu
## Req. python lib.	: kafka-python
##################PARAMETERS################################
bootstrap_serverList='10.10.10.64:19093,10.10.10.65:19093,10.10.10.66:19093'
ftsTopicName='syncApp'
consumerGroupId='consumerGroup'
myColleagueServerList=['20.20.20.27','20.20.20.28']
remoteDCContactServerList=['30.30.30.140','30.30.30.141','30.30.30.142']
remoteDCContactServerCounter=0
remoteDCContactServer=remoteDCContactServerList[remoteDCContactServerCounter]
writeLogFile=True
appLogFile='/data/admin/syncApp/syncDir.log'
unCopiedFiles='/data/admin/syncApp/unCopiedFilesName'
colleagueCounter=0
myCounter=0
rootDir='/mainDir'
##################PARAMETERS################################
import kafka,os,commands
from time import *
from string import *
def maskFileName(fName):
	lenFileName=len(fName)
	if (lenFileName>20):
		return fName[:lenFileName-15]+'**********'+fName[lenFileName-7:]
	elif(lenFileName>10):
		return fName[:lenFileName-8]+'**********'+fName[lenFileName-2:]
	else:
		return fName
def getDatetime():
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
def fileClearWrite(file, writeText):
	try :
		fp=open(file,'w')
		fp.write(writeText+'\n')
		fp.close()
	except :
		print ('!!! An error is occurred while writing file !!!')		
def fileRead(file):
	returnTEXT=''
	if(os.path.exists(file)):
		try :
			fp=open(file,'r')
			returnTEXT=fp.readlines()
			fp.close()
			return returnTEXT
		except :
			print ('!!! An error is occurred while reading file !!!')
			return returnTEXT	
def logWrite(logFile,logText):
	if(writeLogFile):
		print (logText)
		logText='* ('+getDatetime()+') '+logText
		fileAppendWrite(logFile,logText)		
	else:
		print (logText)			
def localUnCopiedFileSender(myFile):
	myNewUnsendedFiles=''	
	myFileNames=fileRead(myFile)
	if(os.path.exists(myFile)):
#		myFileNames=myFileList.split('\n')
		for myFileName in myFileNames:
			if(len(myFileName)>1):
				scpResult=1
				myFileName=myFileName.replace('\n','')
				if(upper(myFileName[:6])=='UPLOAD'):
					scopyResult=os.system('scp -q -o "StrictHostKeyChecking no" -o "ConnectTimeout=5" '+rootDir+str(myFileName[7:])+' '+str(remoteDCContactServerList[remoteDCContactServerCounter])+':'+rootDir+str(myFileName[7:])+'')
				elif(upper(myFileName[:6])=='DELETE'):
					scopyResult=os.system('ssh -q -o "StrictHostKeyChecking no" -o "ConnectTimeout=5" '+str(remoteDCContactServerList[remoteDCContactServerCounter])+' -C "rm -f '+rootDir+str(myFileName[7:])+'"')				
#				scpResult=os.system('scp -q -o "StrictHostKeyChecking no" -o "ConnectTimeout=3" '+rootDir+str(myFileName)+' '+str(remoteDCContactServerList[remoteDCContactServerCounter])+':'+rootDir+str(myFileName.value)+'')
				if ( scopyResult==0 ):
					logWrite(appLogFile,' Copy OK : File -> '+maskFileName(str(myFileName))+' is proccesed. Checked from control file')
				else:
					myNewUnsendedFiles+=myFileName+'\n'
					logWrite(appLogFile,'!!! scp Error !!!! File -> '+maskFileName(str(myFileName))+' is NOT proccesed !!! Checked from control file')
		if(myNewUnsendedFiles==''):
			os.remove(myFile)
		else:
			fileClearWrite(myFile, myNewUnsendedFiles[:len(myNewUnsendedFiles)-1])
			logWrite(appLogFile,' Warning : Some file(s) is/are not copied. That file(s)  is/are written. -> '+myFile)
def remoteUnCopiedFileSender(myFile):
	myNewUnsendedFiles=''
	for myColleagueServer in myColleagueServerList:
		isOK,comResponse = commands.getstatusoutput('ssh -q -o "StrictHostKeyChecking no" -o "ConnectTimeout=3" '+myColleagueServer+' -C  "cat '+myFile+' "')
		if (isOK==0):
			logWrite(appLogFile,' Warning : unCopiedFiles found on remote server -> '+str(myColleagueServer)+'. I will try to procces it.')
			rmFileResult=os.system('ssh -q -o "StrictHostKeyChecking no" -o "ConnectTimeout=3" '+myColleagueServer+' -C  " rm -f '+myFile+'"')
			if(rmFileResult==0):
				logWrite(appLogFile,'OK remote ('+str(myColleagueServer)+') server : File -> '+maskFileName(str(myFile))+' was deleted.' )
			else:
				logWrite(appLogFile,'!!!Error !!!  remote ('+str(myColleagueServer)+') server : File -> '+maskFileName(str(myFile))+' was NOT deleted !!!' )
			myFileNames=comResponse.split('\n')
			for myFileName in myFileNames:
				if(len(myFileName)>1):
					scpResult=1
					myFileName=myFileName.replace('\n','')
					if(upper(myFileName[:6])=='UPLOAD'):
						scopyResult=os.system('scp -q -o "StrictHostKeyChecking no" -o "ConnectTimeout=5" '+rootDir+str(myFileName[7:])+' '+str(remoteDCContactServerList[remoteDCContactServerCounter])+':'+rootDir+str(myFileName[7:])+'')
					elif(upper(myFileName[:6])=='DELETE'):
						scopyResult=os.system('ssh -q -o "StrictHostKeyChecking no" -o "ConnectTimeout=5" '+str(remoteDCContactServerList[remoteDCContactServerCounter])+' -C "rm -f '+rootDir+str(myFileName[7:])+'"')				
#					scpResult=os.system('scp -q -o "StrictHostKeyChecking no" -o "ConnectTimeout=3" '+rootDir+str(myFileName)+' '+str(remoteDCContactServerList[remoteDCContactServerCounter])+':'+rootDir+str(myFileName)+'')
					if ( scopyResult==0 ):
						logWrite(appLogFile,' Copy OK : File -> '+maskFileName(str(myFileName))+' is proccesed. Checked from remote('+str(myColleagueServer)+') control file')
					else:
						myNewUnsendedFiles+=myFileName+'\n'
						logWrite(appLogFile,'!!! scp Error !!!! File -> '+maskFileName(str(myFileName))+' is NOT proccesed !!! Checked from remote('+str(myColleagueServer)+') control file')
		else:
			logWrite(appLogFile,' NAP :No remote('+str(myColleagueServer)+') unCopiedFile.')
	if(myNewUnsendedFiles!=''):
		fileAppendWrite(myFile, myNewUnsendedFiles)			
####### Main program #######
myFileConsumer= kafka.KafkaConsumer(group_id=consumerGroupId,bootstrap_servers=bootstrap_serverList)
myFileConsumer.subscribe([ftsTopicName])
#myPID=os.getpid()
#fileClearWrite(myPIDFILE, str(myPID))
for  myFileName in myFileConsumer:
	scopyResult=1
	if(upper(myFileName.value[:6])=='UPLOAD'):
		scopyResult=os.system('scp -q -o "StrictHostKeyChecking no" -o "ConnectTimeout=5" '+rootDir+str(myFileName.value[7:])+' '+str(remoteDCContactServerList[remoteDCContactServerCounter])+':'+rootDir+str(myFileName.value[7:])+'')
	elif(upper(myFileName.value[:6])=='DELETE'):
		scopyResult=os.system('ssh -q -o "StrictHostKeyChecking no" -o "ConnectTimeout=5" '+str(remoteDCContactServerList[remoteDCContactServerCounter])+' -C "rm -f '+rootDir+str(myFileName.value[7:])+'"')
	if ( scopyResult==0 ):
		logWrite(appLogFile,' Copy OK : File -> '+maskFileName(str(myFileName.value))+' is proccesed. From Kafka')
		if( myCounter==11 ):
			myCounter=0
			localUnCopiedFileSender(unCopiedFiles)
		else:
			myCounter+=1	
		if( colleagueCounter==161 ):
			colleagueCounter=0
			remoteUnCopiedFileSender(unCopiedFiles)
		else:
			colleagueCounter+=1
	else:		
		logWrite(appLogFile,'!!! scp Error !!!! File -> '+str(myFileName.value)+' is NOT proccesed !!!')
		fileAppendWrite(unCopiedFiles, str(myFileName.value))
		if(remoteDCContactServerCounter<len(remoteDCContactServerList)-1):
			remoteDCContactServerCounter+=1
			logWrite(appLogFile,'!!! Warning !!!! New remote DC contact Server -> '+str(remoteDCContactServerList[remoteDCContactServerCounter])+'')
		else:
			remoteDCContactServerCounter=0

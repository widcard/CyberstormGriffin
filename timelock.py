#######################
##Name:Chaoqun Yu
##Program:Timelock
##Version:2.7/3.7/3.8
#######################
import time
from sys import stdin
import datetime
import pytz 
from hashlib import *


DEBUG = True
useCustomSysTime = False

#determine if to use custom system time and, if so, what it should be
Current_Time = "2017 03 23 18 02 06"

#how long (in seconds) a code would be valid for
ValidTime = 60


################################################################################

#convert a time string (formatted YYYY MM DD HH mm SS) into UTC
def toUTC(timeString):
        #convert string into time struct, then convert the struct to
        #UTC time since epoch to return
        timeStruct = time.strptime(timeString, "%Y %m %d %H %M %S")
        return int(time.mktime(timeStruct))


#retrieve the hex value to use for retrieving the code
def getHex():
        
        #retrieve time from stdin and convert it to UTC
        epochTime = toUTC(stdin.read().strip('\n'))
        
        #determine whether to use custom or real system time
        if (useCustomSysTime):
                systemTime = toUTC(Current_Time)
        else:
                dateTime = datetime.datetime.now()
                systemTime = toUTC("{} {} {} {} {} {}".format(dateTime.year, dateTime.month, \
                                dateTime.day, dateTime.hour, dateTime.minute, dateTime.second))

        #compute unadjusted time elapsed
        delta_time = systemTime - epochTime
        #adjust time elapsed based on how long (in seconds) the code is valid for
        interval = delta_time % ValidTime
        
        #get the true (adjusted) time elapsed converted to hex with md5
        #to return for retrieving the code
        hash_time = delta_time - interval
        if(DEBUG):
                print(delta_time)
                print(hash_time)
        h = md5()
        h.update(str(hash_time).encode('utf-8'))
        f = h.hexdigest()
        if(DEBUG):
                print(f)
        m = md5()
        m.update(str(f).encode('utf-8'))
        
        s=m.hexdigest()
        return (s)
        


#use a hex string to retrieve the secret code (first two letters a-f from left
#to right and first two numbers 0-9 from right to left)
def getCode(hexString):
        #show full hexstring for debugging
        if(DEBUG):
                print(hexString)
        
        #setup strings for holding the letters and numbers found in the hex
        alpha = ""
        nums = ""

        #retrieve the first 4 letters from left to right
        for i in hexString:

                #append the letter found to the end of the alpha string
                if (i.isalpha()):
                        alpha += i
                        
                        #once four letters are found, no longer need anymore
                        if(len(alpha) >= 4):
                                break
                        
        #retrieve the first 4 numbers from right to left
        for i in range(len(hexString)-1, -1, -1):
                
                #append the number found to the end of the nums string
                if (not hexString[i].isalpha()):
                        nums += hexString[i]
                        
                        #once four numbers are found, no longer need anymore
                        if(len(nums) >= 4):
                                break

        #retrieve the four digit code, handling special cases of not having enough
        #digits or letters retrieved from the hex string
        if(len(alpha) >= 2 and len(nums) >= 2):
                #no special case needed
                code = alpha[:2] + nums[:2]

        elif(len(alpha) < 2):
                #combine all of the letters and numbers in the string, removing an
                #extra number from the end if there is one (index 5 if len(alpha) == 1)
                code = alpha + nums
                code[:4]
                
        else:
                #not enough numbers, so either use three letters if there is one number,
                #or all letter if no numbers
                if(len(nums) == 1):
                        code = alpha[:3] + nums
                else:
                        code = alpha

        #send resulting 4-digit code to stdout
        code += hexString[15]
        code += hexString[16]
        print(code)


###############################MAIN#############################################
getCode(getHex())

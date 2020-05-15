###################
#@Author:Chaoqun Yu
#Version:3.7
#CWID:102-42-826
##################
from ftplib import FTP

def Ftp(FOLDER):
    IP = "jeangourd.com"
    PORT = 8008 #new port number from decode program1
    contents = []
    USER = "valkyrie"
    PASSWORD ="chooseroftheslain"
    folder ="/.secretstorage/.folder2/.howaboutonemore"
    
     
    ftp = FTP()#create short cut for ftp
    ftp.connect(IP,PORT)#connet to server
    
    ftp.login(USER,PASSWORD)# login using encrypt message,PASSWORD from program 2
    ftp.cwd(folder)#change into the folder that contain files
    ftp.dir(contents.append)#add dir info into contents[]
    ftp.quit()#ftp off
    message= ''

    #Read 7 right most digit or unitizing all ten digit
    for row in contents:
            if FOLDER == "10":
                message += (row[0:10])
            else:
                if row[0:3]== "---":
                    message += (row[3:10])
    #print(message)

    # Read segment of the string and convert to binary
    binary = ''
    for i in message:
            if (i == "r" or i == "w" or i == "x" or i =="d"):
                binary += "1"
            elif (i == "-"):
                binary += "0"
                
    #decoder from Dr.Gourd
    text =""
    i =0
    
    n = 7     
    while(i<len(binary)):
        b = binary[i:i+n]
        b = int(b,2)
        text += chr(b)
        i += n
        
    print (text)
#print time and data
import datetime
x = datetime.datetime.now()
print(x)
#calls function to Method for dir7 and 10
Ftp("7")
Ftp("10")

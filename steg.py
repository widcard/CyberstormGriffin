#######################################################################################################
# Name: Chaoqun Yu
# Date: 5/8/2020						                
# Program: Steg							 
# Version: 2.7						                                                                   
#######################################################################################################

import sys
#debug mod
DEBUG = False

#general usage message
GENERAL_USAGE = "General Usage: ./steg.py -(sr) -(bB) -o<val> [-i<val>] -w<val> [-h<val>]"
STORAGE_USAGE = "Store Data Usage: ./steg.py -(sr) -(bB) -o<val> [-i<val>] -w<val> -h<val>"

#sentinel value for keeping track of where the data ends
SENTINEL = [0,255,0,0,255,0]

#if sentinel is changed, any pieces of code using the length of the sentinel can be automatically adjusted
SEN_LENGTH = len(SENTINEL)

################################################################################

#process the storage (hiding) of data into a wrapper file
def storeData(wrapper, offset, interval):

	#setup for either method:
	#retrieve file to hide inside of wrapper
	hidden = getHidden()
	
	#turn wrapper into list to allow for changing of chars at indexes
	wrapper = list(wrapper)

	#use byte or bit method based on args, otherwise specify usage
	if(sys.argv[2] == "-B"):
		
		#byte method:
		#store the bytes of the hidden file first into the wrapper
		for i in range(len(hidden)):
			wrapper[offset] = hidden[i]
			offset += interval

		#then store the sentinel into the wrapper [MAY NEED TO CHNAGE, WHAT IF DONT USE SENTINEL CAUSE HIDDEN BIG ENOUGH]
		for i in range(SEN_LENGTH):
			wrapper[offset] = chr(SENTINEL[i])
			offset += interval


	elif(sys.argv[2] == "-b"):
		
		#bit method:
		#store a byte one bit at a time by replacing the LSBs of 8 bytes in the wrapper with the
		#8 bits of a byte from the hidden file (append sentienl to end of hidden file for easy access)
		for i in range(SEN_LENGTH):
			hidden += chr(SENTINEL[i])
			
		hidden = list(hidden)
		for i in range(len(hidden)):
			#get int version of hidden byte in var to avoid repeated conversions between chr and int
			curHidden = ord(hidden[i])
			for j in range(8):
				#store current wrapper byte as int to avoid repeated conversions
				curWrapper = ord(wrapper[offset])
				curWrapper &= 11111110
				curWrapper |= ((curHidden & 10000000) >> 7)
				curHidden <<= 1
				#set value of wrapper at offset to the new character
				wrapper[offset] = chr(curWrapper)
				offset += interval

				
	#inform user of proper way to use command line arguments             
	else:
		print(STORAGE_USAGE)
		exit()


	#display results of either method
	print("".join(wrapper))
	if(DEBUG):
		
		#for debugging, print out the integer representation and char value of each byte, 1 per line
		#(recommended to comment out print(hiddenData) for easier viewing)
		hiddenOrd = ""
		for i in range(len(hiddenData)):
			hiddenOrd += str(ord(hiddenData[i])) + " " + hiddenData[i] + "\n"
		print(hiddenOrd)
		

#process the retrieval of data from
def retrieveData(wrapper, offset, interval):

	#general setup for either method:
	#setup string to hold retrieved hidden bytes from the wrapper
	hiddenData = ""
	
	#keep track of if sentinel was found
	found = False

	#use byte or bit method based on args, otherwise specify usage
	if(sys.argv[2] == "-B"):
		
		#byte method:	
		#continue to loop until the sentienl is found, or once the entire wrapper has been traversed
		while (not found and len(wrapper) > offset):

			#add the byte from the wrapper at the offset to the hidden data, increasing offset by interval after
			hiddenData += str((wrapper[offset]))
			offset += interval

			#only attempt to check for sentinel once enough data has been retrieved for it to possibly be there
			if(len(hiddenData) >= SEN_LENGTH):

				#check to see if the seninel was found
				for i in range(SEN_LENGTH):

					#stop checking once a digit of hidden data doesn't match sentinel
					if(ord(hiddenData[i-SEN_LENGTH]) != SENTINEL[i]):
						break

					#once all pieces of the sentienl were found, remove them from the hidden data string
					#and set found to true
					elif(i == SEN_LENGTH-1):
						hiddenData = hiddenData[:-SEN_LENGTH]
						found = True
						
					
	elif(sys.argv[2] == "-b"):
		
		#bit method:
		#continue to loop until the sentienl is found, or once the entire wrapper has been traversed (if
		#there are not eight more bytes (byte at offset and next 7 bytes) then there is nothing left to traverse)
		while (not found and len(wrapper) > offset + 7):

			#hold the resulting byte retrieved from the 8 ending bits
			hiddenByte = 0
			for i in range(8):
				
				#and the wrapper byte with 1 to only get the value of the least significant bit
				bit = ord(wrapper[offset]) & 1
				
				#or the wrapper byte with the current status of the hidden byte to change the LSB
				#of the hiddenByte to the proper bit without changing the remaining bits
				hiddenByte |= bit
				
				#expect for the 8th bit (since it's the last one), shift the hidden byte 1 to the
				#left to make room for the remaining bits
				if(i < 7):
					hiddenByte <<= 1

				#increment the offset by the interval to look at the next appropriate wrapper byte     
				offset += interval

				
			#add the newly formed hidden byte to the hidden data string
			hiddenData += chr(hiddenByte)
			
			#only attempt to check for sentinel once enough data has been retrieved for it to possibly be there
			if(len(hiddenData) >= SEN_LENGTH):

				#check to see if the seninel was found
				for i in range(SEN_LENGTH):   
					if(ord(hiddenData[i-SEN_LENGTH]) != SENTINEL[i]):
						break

					#once all 6 pieces of the sentienl were found, remove them from the hidden data string and set found to true
					elif(i == SEN_LENGTH-1):
						hiddenData = hiddenData[:-SEN_LENGTH]
						found = True
				

	#inform user of proper way to use command line arguments                                    
	else:
		print(GENERAL_USAGE)
		exit()


	#finishing steps for either method:
	#send hidden data to standard output
	print(hiddenData)
	if(DEBUG):
		
		#for debugging, print out the integer representation and char value of each byte, 1 per line
		#(recommended to comment out print(hiddenData) for easier viewing)
		hiddenOrd = ""
		for i in range(len(hiddenData)):
			hiddenOrd += str(ord(hiddenData[i])) + " " + hiddenData[i] + "\n"
		print(hiddenOrd)


#retrieve file to hide inside of wrapper from current directory based on command line arg              
def getHidden():
	if(sys.argv[-1][:2] == "-h"):
		#remove trailing newline inserted from opening
		return open(sys.argv[-1][2:], 'rb').read()[:-1]

	#inform user that hidden file is required for storage mode
	else:
		print(STORAGE_USAGE)
		exit()


#ensure a wrapper file was provided in command line arg from current directory and open it	
def getWrapper():
	if(sys.argv[-1][:2] == "-w"):
		#remove trailing newline inserted from opening
		return open(sys.argv[-1][2:], 'rb').read()[:-1]
	
	elif(sys.argv[-2][:2] == "-w"):
		#remove trailing newline inserted from opening
		return open(sys.argv[-2][2:], 'rb').read()[:-1]

	#inform user of proper usage and exit
	else:
		print(GENERAL_USAGE)
		exit()


#ensure interval was specified and return its value if so		
def getInterval():

	#return the interval if found
	if(sys.argv[4][:2] == "-i"):
		return int(sys.argv[4][2:])

	#use a default interval of 1 otherwise
	else:
		return 1


#ensure an offset was specified and return its value if so   
def getOffset():

	#return the offset if found
	if(sys.argv[3][:2] == "-o"):
		return int(sys.argv[3][2:])

	#inform user of proper usage and exit
	else:
		print(GENERAL_USAGE)
		exit()


###############################MAIN#############################################

#read in arguments from the command line, specifying proper usage if necessary	
if(len(sys.argv) < 5):
	print(GENERAL_USAGE)
	exit()

#ensure wrapper file provided (needed regardless of method used)
wrapper = getWrapper()

#ensure offset specified
offset = getOffset()

#get interval from args (or use 1 if none provided, common for bit method)
interval = getInterval()

#go to the appropriate function to store (hide) data or retrieve it
if(sys.argv[1] == "-s"):
	storeData(wrapper, offset, interval)
elif(sys.argv[1] == "-r"):
	retrieveData(wrapper, offset, interval)

#invalid mode specified
else:
	print(GENERAL_USAGE)

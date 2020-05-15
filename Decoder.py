#!python3.7
from sys import stdin

#decoder funcion
def decoder(binary,n):
    text = ""
    i =  0
    
    while(i<len(binary)):
          b = binary[i:i+7]
          b = int(b,2)
          text += chr(b)
          i += 7
          b = binary[i:i+8]
          b = int(b,2)
          text += chr(b)
          i += 8
    return text

binary = stdin.read().rstrip("\n")
#covert 7 bit
if(len(binary)%7 == 0):
    text = decoder(binary, 7)
    print ("7bit:")
    print (text)
#conver 8 bit
if(len(binary)%8 == 0):
    text = decoder(binary, 8)
    print ("8bit:")
    print (text)



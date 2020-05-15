###################################
##Name:Chaoqun YU
##CWID:10242826
##Program Name:XOR.py
##Version:2.7
###################################
import os
import sys
###############################MAIN#############################################
#read in plaintext or ciphertext binary file
m = sys.stdin.read()

#retrieve binary data from the "key" binary file in same directory
#as this python file
k = open('key', 'rb').read()

result = ""

#loop through each byte (character) in the message text m and xor with the corresponding
#index from the key k
for i in range(len(m)):
    #key can be shorter than the length of the message, so mod by the length of the key to
    #loop around as needed
    result += chr(ord(m[i]) ^ ord(k[i%len(k)]))

#send resulting text to stdout
print(result)

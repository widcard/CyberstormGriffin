#Python3.7 @Chaoqun
import sys
import fileinput
def keyGenerate(stringMy, mykey): 
    
    textSize = len(stringMy)

    keyNew = ""

    i = 0
    j = 0
    while i < textSize:
    	if ord(stringMy[i].upper()) >= 65 and ord(stringMy[i].upper()) <= 91:
    		keyNew = keyNew + mykey[j]
    		j = j + 1
    		if j >= len(mykey):
    			j = 0
    	else:
    		keyNew = keyNew + " "
    	i = i + 1

    return keyNew[0:textSize]


def encrypt(stringMy, key):
	out = ""
	for i in range(len(key)):
		ch = stringMy[i].upper()#match the message and key in the Vigenere table
		if ord(ch) >= 65 and ord(ch) <= 91:
			outCh =  (ord(ch) + ord(key[i].upper())) % 26
			if ord(stringMy[i]) < 97:
				out += chr(outCh + ord('A'))#uppercase
			else:
				out += chr(outCh + ord('a'))#lowercase
		else:
			out += ch#for character that not in the alphabeat
	return out
#same logic as encrpyt
def decrypt(stringMy, key):
	out = ""
	for i in range(len(key)):
		ch = stringMy[i].upper()
		if ord(ch) >= 65 and ord(ch) <= 91:
			outCh =  (ord(ch) - ord(key[i].upper()) + 26) % 26
			if ord(stringMy[i]) < 97:
				out += chr(outCh + ord('A'))
			else:
				out += chr(outCh + ord('a'))
		else:
			out += ch
	return out



def checkArguments():
	if len(sys.argv) < 3:#hint for operation
		print("Please enter the command like this: ./vigenere -e MyKeY or ./vigenere -d MyKeY")
		return False
	if sys.argv[1].lower() != '-e' and sys.argv[1].lower() != '-d':
		print("Argument Two Should be -e or -d")
		return False
	return True


def main():
	if (checkArguments() == True):

		myKey = "".join(sys.argv[2].split())

		if sys.argv[1].lower() == "-e":
			if sys.stdin.isatty():
				for inp in sys.stdin:
					inp = inp.rstrip()
					key = keyGenerate(inp, myKey)
					print(encrypt(inp, key))
			else:
				allLines = "".join(sys.stdin.readlines())
				key = keyGenerate(allLines, myKey)
				print(encrypt(allLines, key))

		else:
			if sys.stdin.isatty():
				for inp in sys.stdin:
					inp = inp.rstrip()
					key = keyGenerate(inp, myKey)
					print(decrypt(inp, key))
			else:
				allLines = "".join(sys.stdin.readlines())
				textSize = 0
				key = keyGenerate(allLines, myKey)
				print(decrypt(allLines, key))
			
    
main()

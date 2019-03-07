#!/usr/bin/python3.6

"""The purpose of this assignment is to create a caesar cipher that will
encrypt/decrypt based on arguments provided on the command line or the
selected method in the interactive form of this script. """

import sys
import logging 

"""Set the max key size so that the cipher key doesn't exceed the number of letters in
the alphabet."""
max_key_size = 26

logging.basicConfig(filename='cipher.log', level=logging.INFO,
			format='%(asctime)s:%(levelname)s:%(message)s')

""" This function, and any function starting with get, will only be run
in the interactive form of this script. """
def getMode():
	while True:
		print("Would you like to encrypt 'e' or decrypt 'd'?")
		mode = input().lower()
		if mode == "e" or mode == "d":
			return mode
		else:
			print("Invalid input, please try again:")


def getMessage():
	print("Enter the message to be encrypted/decrypted:")
	return input()

"""This function runs when the user choses to provide the script with a new key
to be used for encryption/decryption. It will overwrite the keyfile with the 
new key, deleting the old one in the process. The user is warned about this in
the getKey function. """
def change_key():
	key = 0
	while True:
		key = int(input("Enter the new key value: "))
		if key >= 1 and key <= max_key_size:
			file = open("keyFile", "w")
			file.write(str(key))
			file.close()
			return key
		else:
			print("The key cannot exceed the max key size of %s" % (max_key_size))

def getKey():
	key = 0 
	print("Do you want to use a new key or use the old one from the key file?")
	choice = int(input("1. New Key | 2. Old Key: "))	
	if choice == 1:
		print("NOTE: This will replace the old key value in the key file.")
		key = change_key()
		return key
	elif choice == 2:
		file = open("keyFile")
		key = int(file.readline().strip())
		file.close()
		return key
	else:
		print("Sorry, I didn't quite catch that.")
		getKey()

"""This is where the actual encryption/decryption happens. If the mode is set to 'd',
the key is simply reversed in order to perform the decryption. The for loop will
iterate over each character in the messsage. If the character is a letter it will
assign the ord for that character to the variable num, which is then concatenated
with the key. It will then shift the character based on wether or not it is upper
or lower case, and then will concatenate the character to the translated_Message 
variable. If the character is not a letter, it will simply concatenate that
charcter to the translated_Message variable, preserving any spaces or special/
non-alphanumeric characters. """
def cryptMessage(mode, key, message):
	translated_Message = " "
	if mode == "d":
		key = -key

	for character in message:
		if character.isalpha():
			num = ord(character)
			num += key

			if character.isupper():
				if num > ord("Z"):
					num -= 26
				elif num < ord("A"):
					num += 26
			elif character.islower():
				if num > ord("z"):
					num -= 26
				elif num < ord("a"):
					num += 26

			translated_Message += chr(num)
		else:
			translated_Message += character 
	return translated_Message

"""The following play and play_again functions are used primarily for flow control while 
being run in the interactive mode. This could have been achieved without the use of 
functions, but the code looks way messier and is much harder to read and 
understand."""
def play_again():
	while True:
		print("Do you want to enter another message to be ciphered? (y/n)")
		start = input().lower()
		if start == "y" or start == "n":
			return start
		else:
			print("Invalid input, please try again.")


def play():
	print("Do you want to enter a message to be ciphered? (y/n)")
	start = input().lower()
	while start == "y":
		mode = getMode()
		message = getMessage()
		key = getKey()

		print("Here is your new message:")
		print(cryptMessage(mode, key, message))
	
		start = play_again()

	if start == "n":
		print("Ok, closing the program...")
	
	if start != "y" and start != "n":
		print("Invalid input, let's try that again shall we...")
		play()

"""Here the program will check to see how many arguments were provided and will decide
if it will be run interactively or non-interactively. If the user provides no arguments,
the script will automatically be run interactively. If the proper amount of arguments 
were supplied, it will bypass all of the get functions and perform the encryption/
decryption process on the supplied message. """
if len(sys.argv) < 4 or len(sys.argv) > 4:
	if len(sys.argv) == 1:
		play()
		logging.info("Cipher started with no arguments, starting interactive mode.")
	elif sys.argv[1] == "-h":
		print("/.caesarCode.py {e|d} key 'text'")
	else:
		print("######################################################################")
		print("Invalid arguments detected, the script will now run in interactive mode.")
		print("#######################################################################")
		play()
		logging.info("Started cipher in interactive mode.")
else:
	print("###############################################################")
	print("Arguments detected, running the script in non-interactive mode.")	
	print("###############################################################")

	mode = sys.argv[1]	
	key = int(sys.argv[2])
	message = sys.argv[3]
	
	logging.info("Started cipher in non-interactive mode.")

	print("Here is your new message:")
	print(cryptMessage(mode, key, message))

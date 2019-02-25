#PasswordManager.py

import os.path
from hashlib import scrypt 
from os import urandom
from base64 import b64encode

def const_equality(hash1, hash2):
    # If lengths are not equal, we know that it is wrong and timing attacks are not an issue
    if (len(hash1) != len(hash2)):
    	return False

    are_different = False

    # iterate over all bytes
    for i in range(0, len(hash1)):
    	# we use |= as it always sets a value (but it may be the same value)
    	# * | true == true, true | * == true, false | false == false
    	# a naive implementation would conditionally set, which is not constant time
    	are_different |= (hash1[i] != hash2[i])

    # Since we are checking for equality, we should not the are_different value
    return not are_different


class passwordHash:
	def do_scrypt(plainPassword, salt, n, r, p):
		return scrypt(plainPassword.encode("utf-8"), salt=salt.encode("utf-8"), n=n, r=r, p=p, maxmem=((n*r)<<8), dklen = (128))
	
	#This method should never be called. If called, there is something wrong with the database.
	def null_hasher(null, null1):
		while True:
			print ("Database corruption detected: Invalid hash algorithm")
			input ("Please restart. Press Ctrl-C")

	def scrypt_hasher(n, r, p):
		return lambda plainPassword, salt : passwordHash.do_scrypt(plainPassword, salt, n, r, p)

	#If it is needed to update the hashing algoritm, adding the next algorithm to this list will automatically upgrade users to the new hashing algorithm
	hashAlgorithms = [
		null_hasher,
		scrypt_hasher(n = 1<<15, r = 8, p = 1)
	]

	currentAlgorithm = len(hashAlgorithms) - 1

	def HashPassword(self, plainPassword, salt, hashver):
		hasher = self.hashAlgorithms[hashver]

		rawhash = hasher(plainPassword, salt)

		str_hashedPassword = b64encode(rawhash).decode("utf-8")
		passwordInfo ={
			"Password": str_hashedPassword,
			"Salt": salt,
			"HashVer": hashver
		}
		return passwordInfo


	#Hashes a password and generates a random salt
	def hashPassword_RandomSalt(self, plainPassword):
		return self.HashPassword(plainPassword, self.GenerateSalt(), passwordHash.currentAlgorithm)


	#Hashes a user input password and checks if the password is correct or not. Returns true or false.
	def hashPassword_check(self, HashedPassword, plainPassword, userHashAlgorithm, salt):
		# TODO: constant time comparison
		login_success = const_equality(self.HashPassword(plainPassword, salt, userHashAlgorithm)["Password"], HashedPassword)

		if not login_success:
			return [False]

		if userHashAlgorithm != self.currentAlgorithm:
			print ("User on wrong hash algorithm. Updating")
			return [True, self.hashPassword_RandomSalt(plainPassword)]
		else:
			return [True, False]
		

	#Method of salt generation
	def GenerateSalt(self):
		rBytes = os.urandom(64)
		salt = b64encode(rBytes).decode("utf-8")[:32]
		return salt



# Legacy password hashing algorithms will have functions defined in the following way
	
	#def LegacyHash_check_*hashAlgorithm*(self, stuff): #comment about what the hash algorithm is
	#	Do stuff()
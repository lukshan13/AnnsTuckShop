#skHanndler.py

import os.path
from os import urandom
from base64 import b64encode

class sk:

	fileSK_exists = None
	key = None

	#checks if secret key file exists
	def checkSKfile(self):
		if (os.path.isfile("ATS/secrets/sk.txt")):
		    self.fileSK_exists = True
		else:
		    self.fileSK_exists = False
		    print ("Secret Key file does not exist)")

	#generates a new key
	def GenerateAndWriteSK(self):
		with open("ATS/secrets/sk.txt","w") as file:
			rBytes = os.urandom(64)
			self.NewKey = b64encode(rBytes).decode('utf-8')[:32]
			file.write(str(self.NewKey))
			file.close()


	def ReadKey(self):
		with open("ATS/secrets/sk.txt","r") as file:
			self.key = file.read()
			print ("KEY LEN:", len(self.key))
			if len(self.key) != 32: #if key stored in txt file is wrong length, it will be purged and a new one will be generated.
				print ("WARNING: SECRET KEY IS INVALID.")
				self.GenerateAndWriteSK()
				return
			file.close()
		



	def run(self):
  		self.checkSKfile()
  		if self.fileSK_exists == False:
  			self.GenerateAndWriteSK()
  		self.ReadKey()

  	#Method is called when user wants to purge the secret key
	def purgeKey(self):
  		print ("WARNING: SECRET KEY IS GOING TO BE PURGED")
  		self.GenerateAndWriteSK()
  		print ("SECRET KEY RESET: ALL SESSIONS ARE NOW INVALIDATED")
  		self.ReadKey()


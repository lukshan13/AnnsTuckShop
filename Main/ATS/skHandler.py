import os.path
from os import urandom
from base64 import b64encode

class sk:

	fileSK_exists = None
	key = None


	def checkSKfile(self):
		if (os.path.isfile("ATS/static/sk.txt")):
		    self.fileSK_exists = True
		else:
		    self.fileSK_exists = False
		    print ("Secret Key file does not exist)")


	def GenerateAndWriteSK(self):
		file = open("ATS/static/sk.txt","w")
		rBytes = os.urandom(64)
		self.NewKey = b64encode(rBytes).decode('utf-8')[:32]
		file.write(str(self.NewKey))
		file.close()


	def ReadKey(self):
		file = open("ATS/static/sk.txt","r")
		self.key = file.read()
		file.close()
		



	def run(self):
  		self.checkSKfile()
  		if self.fileSK_exists == False:
  			self.GenerateAndWriteSK()
  		self.ReadKey()


	def purgeKey(self):
  		print ("WARNING: SECRET KEY IS GOING TO BE PURGED")
  		self.GenerateAndWriteSK()
  		print ("SECRET KEY RESET: ALL SESSIONS ARE NOW INVALIDATED")
  		self.ReadKey()


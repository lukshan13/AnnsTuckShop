from ATS import db
from ATS.models import User, Item, Order


class sUser:

	Username = None
	Password = None
	existing = False
	verified = False
	error = None
	success_login = False
	current_user_login = None

	def __init__(self, Username, Password):

		self.Username = Username
		self.Password = Password


	def normalise(self):
		self.Username = self.Username.lower()



	def check_existing(self):
		
		try:
			check_query = User.query.filter_by(Username=self.Username).first()
			#checking if account exisits
			if check_query.Username == self.Username:
				self.existing = True
				print ("Username found")
				
		except AttributeError:
			self.existing = False
			self.error = ("Username does not exist or is miss-spelt")


	def check_verified(self):
		#Checking if username email verified
		self.current_user_login = User.query.filter_by(Username=self.Username).first()
		if self.current_user_login.AccVerified == (1):
			self.verified = True
			print ("Username email verified")
		else:
			self.error = ("Username email not verified. Please check email to verify account")



	def compare_password(self):
		#Checking password
		if self.current_user_login.Password == self.Password:
			self.success_login = True
			print ("Credentials match!")
		else:
			self.error = ("Incorrect Password")
			
			


	def user_login(self):
		print ("New Login request")
		self.normalise()
		self.check_existing()
		if self.existing == (True): #tells function to continue if account exists
			self.check_verified()
			if self.verified == (True): #tells function to continue if account verified
				self.compare_password()

		print ("Error:", self.error)

		



from ATS import db
from ATS.models import User, Item, Order
from ATS.passwordManager import passwordHash


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
				
		except AttributeError:
			self.existing = False
			self.error = ("Username does not exist or is miss-spelt")


	def check_verified(self):
		#Checking if username email verified
		self.current_user_login = User.query.filter_by(Username=self.Username).first()
		if self.current_user_login.AccVerified == (1):
			self.verified = True
		else:
			self.error = ("Username email not verified. Please check email to verify account. Info: PLEASE CHECK JUNK/SPAM OF YOUR EMAIL")
			


	def compare_password(self):
		#Checking password

		checkPassword = passwordHash()		
		if checkPassword.hashPassword_check(self.current_user_login.Password, self.Password, self.current_user_login.HashVer, self.current_user_login.Salt) == True:
			self.success_login = True
		else:
			self.error = ("Incorrect Password")
			
			


	def user_login(self):
		self.check_existing()
		if self.existing == (True): #tells function to continue if account exists
			self.check_verified()
			if self.verified == (True): #tells function to continue if account verified
				self.compare_password()

		print ("Error:", self.error)

		



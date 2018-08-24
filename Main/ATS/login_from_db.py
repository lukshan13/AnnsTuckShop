from ATS import db
from ATS.models import User, Item, Order


class sUser:

	Username = None
	Password = None
	existing = False
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
			print ("checking if account exisits")
			if check_query.Username == self.Username:
				self.existing = True
				print ("User found")
				
		except AttributeError:
			self.existing = False
			self.error = ("Username does not exist or is misspelt")

	


	def compare_password(self):
		print ("Checking password")
		self.current_user_login = User.query.filter_by(Username=self.Username).first()
		if self.current_user_login.Password == self.Password:
			self.success_login = True
			print ("Credentials match!")
		else:
			self.error = ("Incorrect Password")
			
			


	def user_login(self):
		print ("New Login request")
		self.normalise()
		self.check_existing()
		if self.existing == (True):
			self.compare_password()

		print ("Error:", self.error)

		



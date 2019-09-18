#register_to_db.py

from ATS import db
from ATS.models import User
from ATS.user_verification import GetVerifyToken
from ATS.passwordManager import passwordHash

class rUser:

	EmailAddress = None
	existing = False
	error = None
	token = None

	def __init__(self, FirstName, LastName, Username, EmailEnd, Year, House, Password, Admin):
		self.FirstName = FirstName
		self.LastName = LastName
		self.Username = Username
		self.EmailEnd = EmailEnd
		self.Year = Year
		self.House = House
		self.Password = Password
		self.Admin = Admin

	def check_existing(self):
		
		try:
			check_query = User.query.filter_by(Username=self.Username).first()
			if check_query.Username == self.Username:
				self.existing = True
				self.error = ("Account under that username already exists.")
		except AttributeError: #An attribrute error will occur if that user does not exist
			self.existing = False	

	def generate_email_address(self):
		if self.EmailEnd == ("sch_staff"):
			EmailDomain = "@forest.org.uk"
		if self.EmailEnd == ("sch_student"):
			EmailDomain = "@forestsch.org.uk"

		self.EmailAddress = (self.Username+EmailDomain)

	def normalise(self):
		self.FirstName = self.FirstName.capitalize()
		self.LastName = self.LastName.capitalize()
		self.Username = self.Username.lower()

	def add_to_db(self):
		self.generate_email_address()
		self.getPassword()
		self.new_user_to_add = User(First_name=self.FirstName, Last_name=self.LastName, Username=self.Username, Year=self.Year, Email=self.EmailAddress, House=self.House, Password=self.Password, Salt=self.Salt, HashVer=self.HashVer, Admin_status=self.Admin)
		db.session.add(self.new_user_to_add)
		db.session.commit()

	def getPassword(self):
		hashNewPass = passwordHash()
		PasswordData = hashNewPass.hashPassword_RandomSalt(self.Password)
		self.Password = PasswordData["Password"]
		self.Salt = PasswordData["Salt"]
		self.HashVer = PasswordData["HashVer"]

	def check_username(self):
		return self.Username.isalnum() and self.FirstName.isalnum() and self.LastName.isalnum()


		


	def add_new_user(self):
		self.normalise()
		if self.check_username():
			self.check_existing()
			if self.existing == (False):
				self.add_to_db()
				getVerify = GetVerifyToken(self.Password, self.Username, self.EmailAddress, self.FirstName)
				getVerify.get_verify_token()
				email = getVerify.send_email_verify_token()
				if email != None:
					self.error = ("Something went wrong while emailing you. We have registered you to the system, please talk to Ann to verify your account")
				self.token = getVerify.token
		else:
			self.error = ("Something went wrong whilst carrying out this task. Please ask for help. Your error code is 0x01")

	def admin_add_new_user(self):
		self.normalise()
		self.check_existing()
		if self.existing == (False):
			self.add_to_db()
			self.new_user_to_add.AccVerified = ("1")
			db.session.commit()
			self.token = None

class vUser:

	def __init__(self, vUsername):
		self.Username = vUsername.lower()


	def verify_user(self):
			try:
				check_query = User.query.filter_by(Username=self.Username).first()
				check_query.AccVerified = ("1")
				db.session.commit()
			except AttributeError:
				error = ("Something went wrong, please try again. This should not happen")
				print (error)
				return error

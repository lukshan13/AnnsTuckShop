from ATS import db
from ATS.models import User
from ATS.user_verification import GetVerifyToken


class rUser:

	FirstName = None
	LastName = None
	Username = None
	EmailEnd = None
	YGS = None
	House = None
	EmailAddress = None
	Password = None
	existing = False
	error = None
	token = None

	def __init__(self, FirstName, LastName, Username, EmailEnd, YGS, House, Password):
		self.FirstName = FirstName
		self.LastName = LastName
		self.Username = Username
		self.EmailEnd = EmailEnd
		self.YGS = YGS
		self.House = House
		self.Password = Password


	def check_existing(self):
		
		try:
			check_query = User.query.filter_by(Username=self.Username).first()
			print ("checking if account already exisits")
			if check_query.Username == self.Username:
				self.existing = True
				self.error = ("Account under that username already exists.")
		except AttributeError:
			print ("Account does not exist")
			self.existing = False	


	def generate_email_address(self):
		if self.EmailEnd == ("sch_staff"):
			EmailDomain = "@forest.org.uk"
		if self.EmailEnd == ("sch_student"):
			EmailDomain = "@forestsch.org.uk"

		self.EmailAddress = (self.Username+EmailDomain)
		print ("Generating account for", self.EmailAddress)



	def normalise(self):
		self.FirstName = self.FirstName.capitalize()
		self.LastName = self.LastName.capitalize()
		self.Username = self.Username.lower()



	def add_to_db(self):
		self.generate_email_address()
		new_user1 = User(First_name=self.FirstName, Last_name=self.LastName, Username=self.Username, YGS=self.YGS, Email=self.EmailAddress, House=self.House, Password=self.Password)
		db.session.add(new_user1)
		db.session.commit()


	def add_new_user(self):
		print ("New Register request")
		self.normalise()
		self.check_existing()
		if self.existing == (False):
			self.add_to_db()
			getVerify = GetVerifyToken(self.Password, self.Username, self.EmailAddress, self.FirstName)
			getVerify.get_verify_token()
			getVerify.send_email_verify_token()
			self.token = getVerify.token
	

class vUser:

	Username = None

	def __init__(self, vUsername):
		self.Username = vUsername.lower()

	def verify_user(self):
			try:
				print (self.Username)
				check_query = User.query.filter_by(Username=self.Username).first()
				print (check_query)
				check_query.AccVerified = ("1")
				db.session.commit()
				print ("commiting to db")
			except AttributeError:
				error = ("Something went wrong, please try again. This should not happen")
				print (error)
				return error

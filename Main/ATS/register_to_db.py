from ATS import db
from ATS.models import User, Item, Order


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
				self.error = ("Account under that name already exists.")


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


	def add_to_db(self):
		self.generate_email_address()
		new_user1 = User(First_name=self.FirstName, Last_name=self.LastName, Username=self.Username, YGS=self.YGS, Email=self.EmailAddress, House=self.House, Password=self.Password)
		db.session.add(new_user1)
		db.session.commit()


	def add_new_user(self):
		self.check_existing()
		if self.existing == (False):
			self.add_to_db()
		
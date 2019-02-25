#user_modification.py

from ATS import db
from ATS.models import User
from ATS.passwordManager import passwordHash


class userModification:


	def viewUserToModify(self, username):
		#Finds the user that is about to modified and retrieves information.
		user = User.query.filter_by(Username=username).first()
		self.userData = {
		"Username": user.Username,
		"FirstName": user.First_name,
		"LastName": user.Last_name,
		"Email": user.Email,
		"House": user.House,
		"YGS": user.YGS
		}


	def admin_modify_user(self, FirstName, LastName, Username, EmailEnd, YGS, House, plainPassword, Admin, OGusername):

		#Normalizing inputs
		FirstName = FirstName.capitalize()
		LastName = LastName.capitalize()
		Username = Username.lower()

		if YGS == "None":
			YGS = User.query.filter_by(Username = OGusername).first().Year
			
		if plainPassword != None:
			hashNewPass = passwordHash()
			PasswordData = hashNewPass.hashPassword_RandomSalt(plainPassword)
			self.Password = PasswordData["Password"]
			self.Salt = PasswordData["Salt"]
			self.HashVer = PasswordData["HashVer"]
		else:
			PasswordData = {}

		#Email is created by aggregating Username and emailEnd
		if EmailEnd == ("sch_staff"):
			EmailDomain = "@forest.org.uk"
		if EmailEnd == ("sch_student"):
			EmailDomain = "@forestsch.org.uk"
		EmailAddress = (Username+EmailDomain)




		#data is committed to the database
		data = {"First_name": FirstName, "Last_name": LastName, "Username": Username, "Year": YGS, "Email": EmailAddress, "House" : House, "Admin_status": Admin}
		data.update(PasswordData)
		user_to_modify = User.query.filter_by(Username = OGusername).update(data)
		db.session.commit()


	def standard_modify_user(self, FirstName, LastName, Username, EmailEnd, YGS, House, plainPassword, OGusername):

		#Normalizing inputs
		FirstName = FirstName.capitalize()
		LastName = LastName.capitalize()
		Username = Username.lower()

		if plainPassword != None:
			hashNewPass = passwordHash()
			PasswordData = hashNewPass.hashPassword_RandomSalt(plainPassword)
			self.Password = PasswordData["Password"]
			self.Salt = PasswordData["Salt"]
			self.HashVer = PasswordData["HashVer"]
		else:
			PasswordData = {}

		if YGS == "None":
			YGS = User.query.filter_by(Username = OGusername).first().Year

		#Email is created by aggregating Username and emailEnd
		if EmailEnd == ("sch_staff"):
			EmailDomain = "@forest.org.uk"
		if EmailEnd == ("sch_student"):
			EmailDomain = "@forestsch.org.uk"
		EmailAddress = (Username+EmailDomain)

		#data is committed to the the database
		data = {"First_name": FirstName, "Last_name": LastName, "Username": Username, "Year": YGS, "Email": EmailAddress, "House" : House }
		data.update(PasswordData)
		user_to_modify = User.query.filter_by(Username = OGusername).update(data)
		db.session.commit()
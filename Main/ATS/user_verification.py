from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import url_for
from ATS import mail
from flask_mail import Message

class GetVerifyToken:

	password = None
	username = None
	token = None
	emailAddress = None
	First_Name = None

	def __init__ (self,DBpassword, DBusername, emEmailAdd, emFirstName):
		self.password = str(DBpassword)
		self.username = str(DBusername)
		self.emailAddress = str(emEmailAdd)
		self.First_Name = str(emFirstName)


	def get_verify_token(self, expires_sec=604800):
		username = self.username
		print ("Generating verification token for user")
		s = Serializer(username, expires_sec)
		self.token = (s.dumps(self.password)).decode("utf-8")

	def send_email_verify_token(self):
		msg = Message("Anne's Tuck Shop Account: Email Verification",
			recipients=[self.emailAddress])
		msg.body = f'''Dear {self.First_Name}

Thank you for signing up on Anne's Tuck Shop's web app. As you may know, the site allows you to view current food options as well as give you the ability to pre-order breakfast and quarter items. This makes it easier for Anne to manage food orders. To verify, please click on the link below. It should automatically verify you. If you find yourself unable to verify your email, please go to /verify-manual and enter the following details:

Please note: The token expires in 7 days of creation. If the account is not verified before then, the account will be marked as spam and you will not be able to register with this username again.

http://annstuckshop.sytes.net{url_for('verify_auto', vUsername = self.username, vToken = self.token)}

If you are having trouble using the above link, please navigate to http://annstuckshop.sytes.net/verify-manual and enter the following data

Forest Email Username: {self.username}
Token: {self.token}

Thanks
Ann's Tuck Shop

Created by Lukshan Sharvaswaran, 2018. This is part of an NEA project for computer science, all rights reserved.

		'''
		mail.send(msg)





class CheckVerifyToken:

	token = None
	username = None
	checkedPassword = None
	error = None

	def __init__ (self, wUsername, wToken):
		self.username = str(wUsername).lower()
		self.token = (wToken)

	def check_verify_token(self):
		print (self.username)
		print ("checking token")
		token = self.token
		s = Serializer(self.username)
		print (token)
		print ("checkedPassword = s.loads(token)")
		try:
			self.checkedPassword = s.loads(token)
			return ("Verified")
		except:
			self.error = ("Invalid/Expired token or bad username. If you have an expired token, please contact support to refresh your username from the database")
			return ("self.error")

		print ("after token  ", checkedPassword)
		

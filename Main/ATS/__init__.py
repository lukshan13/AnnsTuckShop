import sys, os
print ("Developed By Lukshan Sharvaswaran, DvDt:2018. @lukshan13")

try:
	print (f"Python Version compatible")
except:
	print ("It looks like your version of Python is not compatible. Please try with Python 3.6.5+")
	while True:
		sys.exit()

print ('importing modules.....')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from ATS import skHandler


import os, sys
site = Flask(__name__)

print("The Python version is %s.%s.%s" % sys.version_info[:3])

key = skHandler.sk()
key.run()

site.config['SECRET_KEY'] = (key.key)
#Key is imported from a file for better security and to easily reset it
site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ats.db'
site.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#calling database

site.config['MAIL_SERVER'] = 'smtp.gmail.com'
site.config['MAIL_PORT'] = 587
site.config['MAIL_USE_TLS'] = True
site.config['MAIL_USERNAME'] = (os.environ.get("EMAIL_USER"))
site.config['MAIL_DEFAULT_SENDER'] = (os.environ.get("EMAIL_USER"))
site.config['MAIL_PASSWORD'] = (os.environ.get("EMAIL_PASS"))

print ("SMTP server is : ", os.environ.get("EMAIL_USER"))
#Gmail username and password is being stored in enviromental variables to prevent access on repositories, and makes it much easier to change.
#SMTP server will be switched to the forest.org.uk's server in due course once it is available


db = SQLAlchemy(site)
login_manager = LoginManager(site)
mail = Mail(site)

from ATS import getInfo as getInfo
from ATS import routes
from ATS.DB_check import check_breakfast, check_quarter


db.create_all()
checkBreakfast = check_breakfast()
checkQuarter = check_quarter()
checkBreakfast.checkBreakfast()
checkQuarter.checkQuarter()



print (getInfo.time_display)
print (getInfo.TimeOfDay, "'Ann's Tuck Shop' site flask server is now running. Please navigate to the address below to access the site.")

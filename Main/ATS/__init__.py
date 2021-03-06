#__init__.py

import sys, os
print ("Developed By Lukshan Sharvaswara, 2017-2019. @lukshan13. Licenced under GLU v3.0.")

#Checks if the python version is 3.7.1 or above
try:
	print (f"Python Version compatible")
	from hashlib import scrypt
except:
	print ("It looks like your version of Python is not compatible. Please try with Python 3.7.1 or above")
	while True:
		sys.exit()

print ('importing modules.....')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from ATS import skHandler



import os, sys
csrf = CSRFProtect()
site = Flask(__name__)
csrf.init_app(site)


print("The Python version is %s.%s.%s" % sys.version_info[:3])

#obtains secret key from .txt file. Will generate one if not found.
key = skHandler.sk()
key.run()

site.config['SECRET_KEY'] = (key.key)
site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ats.db'
site.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#database

site.config['MAIL_SERVER'] = 'smtp.gmail.com'
site.config['MAIL_PORT'] = 587
site.config['MAIL_USE_TLS'] = True
site.config['MAIL_USERNAME'] = (os.environ.get("EMAIL_USER"))
site.config['MAIL_DEFAULT_SENDER'] = (os.environ.get("EMAIL_USER"))
site.config['MAIL_PASSWORD'] = (os.environ.get("EMAIL_PASS"))

print ("SMTP server is : ", os.environ.get("EMAIL_USER"))
#Gmail username and password is being stored in enviromental variables for added security, and makes it much easier to change.
#SMTP server will be switched to the forest.org.uk's server in due course once it is available


db = SQLAlchemy(site)
login_manager = LoginManager(site)
mail = Mail(site)

from ATS import getInfo as getInfo
from ATS import routes
from ATS.DB_check import check_breakfast, check_quarter, check_default_entries

#Calls functions that will check the interity of the database
db.create_all()
checkBreakfast = check_breakfast()
checkQuarter = check_quarter()
checkBreakfast.checkBreakfast()
checkQuarter.checkQuarter()

checkEntries = check_default_entries()
checkEntries.check_admin()
checkEntries.check_none_item()

print (getInfo.time_display)
print (getInfo.TimeOfDay, "'Ann's Tuck Shop' site flask server is now running. Please navigate to the address below to access the site.")
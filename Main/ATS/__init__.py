print ("Developed By Lukshan Sharvaswaran, DvDt:2018. @lukshan13")

print ('importing modules.....')
import sys, os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from ATS import getInfo as getInfo
from ATS import skHandler


import os, sys
site = Flask(__name__)

print("The Python version is %s.%s.%s" % sys.version_info[:3])

key = skHandler.sk()
key.run()

site.config['SECRET_KEY'] = (key.key)
#temp secret key for developmental purposes
site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
site.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#site.config['MAIL_SERVER'] = 'smtp.gmail.com'
#site.config['MAIL_PORT'] = 587
#site.config['MAIL_USE_TLS'] = True
#site.config['MAIL_USERNAME'] = (os.environ.get("EMAIL_USER"))
#site.config['MAIL_DEFAULT_SENDER'] = (os.environ.get("EMAIL_USER"))
#site.config['MAIL_PASSWORD'] = (os.environ.get("EMAIL_PASS"))
#Due to current gmail issues (my account got blocked because i tried to send a message without telling google i was going to), I'm temporarily going to use my outlook account


site.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
site.config['MAIL_PORT'] = 587
site.config['MAIL_USE_TLS'] = True
site.config['MAIL_USERNAME'] = YOUR EMAIL HERE
site.config['MAIL_DEFAULT_SENDER'] = YOUR EMAIL HERE
site.config['MAIL_PASSWORD'] = YOUR PASSWORD HERE



print ("SMTP server is : ", os.environ.get("EMAIL_USER"))
#Gmail username and password is being stored in enviromental variables to prevent access on repositories, and makes it much easier to change.
#SMTP server will be switched to the forest.org.uk's server in due course once it is available


db = SQLAlchemy(site)
login_manager = LoginManager(site)
mail = Mail(site)




from ATS import routes


print (getInfo.time_display)
print (getInfo.TimeOfDay, "'Ann's Tuck Shop' site flask server is now running. Please navigate to the address below to access the site.")

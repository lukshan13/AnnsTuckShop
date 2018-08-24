print ("Developed By Lukshan Sharvaswaran, DvDt:2018. @lukshan13")

print ('importing modules.....')
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from ATS import getInfo as getInfo


import os, sys
site = Flask(__name__)

print("The Python version is %s.%s.%s" % sys.version_info[:3])


site.config['SECRET_KEY'] = '123456789abcdefghijk987654321'
#temp secret key for developmental purposes
site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
site.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(site)
login_manager = LoginManager(site)

from ATS import routes


print (getInfo.time_display)
print (getInfo.TimeOfDay, "'Ann's Tuck Shop' site flask server is now running. Please navigate to the address below to access the site.")

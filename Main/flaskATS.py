print ("Developed By Lukshan Sharvaswaran, DvDt:2018. @lukshan13")

#calling in required libraries for code
import flask
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import getInfo as getInfo
import os, sys
site = Flask(__name__)

print("The Python version is %s.%s.%s" % sys.version_info[:3])


site.config['SECRET_KEY'] = '123456789abcdefghijk987654321'
#temp secret key for developmental purposes
site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
site.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(site)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	First_name = db.Column(db.String(25), unique=True, nullable=False)
	Last_name = db.Column(db.String(25), unique=True, nullable=False)
	Username = db.Column(db.String(25), unique=True, nullable=False)
	YGS = db.Column(db.Integer, nullable=False)
	Email = db.Column(db.String(120), unique=True, nullable=False)
	House = db.Column(db.String(10), nullable=False)
	Password = db.Column(db.String(120), nullable=False)
	Orders = db.relationship('Order', backref=('customer'), lazy=True)


class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Item_name = db.Column(db.String(25), unique=True, nullable=False)
	Type = db.Column(db.String(8), nullable=False)
	Price = db.Column(db.Integer, nullable=False)


class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	User_ID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	Order_Item = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
	






#hardcoding values incase no values are returned from database to prevent errors



#from getInfo 
getInfo.RunGetInfo()
'''TEMP'''
userType = ("Guest")
page_title = (userType + ": ")

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    func()

def ParseInfo():
	global info
	getInfo.RunGetInfo()
	info = {
		'page_title': (page_title),
		'date' :(getInfo.date),
		'day': (getInfo.day),
		'TimeOfDay': (getInfo.TimeOfDay),
		'AccademicYear12': (getInfo.StartYear12),
		'AccademicYear13': (getInfo.StartYear13)
	}

@site.route('/home')
@site.route('/')
def home():
	ParseInfo()
	return render_template('Home.html',info=info, pg_name="Home", sidebar="yes")

@site.route('/signup/', methods=['POST', 'GET'])
def gotoregister():
	return redirect(url_for('register'), 301)

@site.route('/register/', methods=['POST', 'GET'])
def register():
	ParseInfo()
	global First_Name
	
	if request.method == 'POST':
		First_Name = request.form 
		print (First_Name)
		print ("test")

	return render_template('Signup.html',info=info, pg_name="Sign Up")

@site.route('/signin/')
def signin():
	ParseInfo()
	return render_template('Signin.html',info=info, pg_name="Sign In")




@site.route('/about')
def about():
	ParseInfo()
	return render_template('About.html')

@site.route('/shutdownserver1034')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'



#enabling debug mode and hosts when executed via python module
if __name__ == '__main__':
	site.run(debug=True)
	site.run(host='0.0.0.0')


print (getInfo.time_display)
print (getInfo.TimeOfDay, "'Ann's Tuck Shop' site flask server is now running. Please navigate to the address below to access the site.")



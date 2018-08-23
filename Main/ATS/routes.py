from flask import render_template, url_for, request, redirect
from ATS import site, db

from ATS.models import User, Item, Order
from ATS.register_to_db import rUser
import ATS.getInfo as getInfo




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
	
	if request.method == 'POST':
		global new_user
		form_data = request.form
		new_user = rUser(form_data['First_Name_Form'], form_data['Last_Name_Form'], form_data['Forest_Username_Form'], form_data['Forest_Email_Domain_Form'], form_data['AccademicYear_Form'], form_data['House_Form'], form_data['Password_Form'],)
		new_user.add_new_user()
		if new_user.error == "Account under that name already exists.":
			print (new_user.error)
			return redirect(url_for('error'), 302)
		return redirect(url_for('home'), 301)




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

@site.route('/error/')
def error():
	ParseInfo()
	return render_template('Error.html',info=info, pg_name="Error", ErMsg=new_user.error)
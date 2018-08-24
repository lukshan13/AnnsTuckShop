from flask import render_template, url_for, request, redirect
from flask_login import login_user, current_user, logout_user
from ATS import site, db

from ATS.models import User, Item, Order
from ATS.register_to_db import rUser
from ATS.login_from_db import sUser
from ATS.skHandler import sk

from ATS import getInfo as getInfo




#from getInfo 
getInfo.RunGetInfo()
'''TEMP'''

page_title = ("Guest" + ": ")

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    func()

def ParseInfo():


	global info
	try:
		if current_user.YGS:
			if current_user.YGS != "S":
				user_type = ("Student")
			else:
				user_type = ("Staff")
	except:
		user_type = ("Guest")

	page_title = (user_type + ": ")
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
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	ParseInfo()

	if request.method == 'POST':
		global login_s_error
		form_data = request.form
		new_user = rUser(form_data['First_Name_Form'], form_data['Last_Name_Form'], form_data['Forest_Username_Form'], form_data['Forest_Email_Domain_Form'], form_data['AccademicYear_Form'], form_data['House_Form'], form_data['Password_Form'])
		new_user.add_new_user()
		if new_user.error != None:
			print (new_user.error)
			login_s_error = new_user.error
			return redirect(url_for('error'), 302)
		return redirect(url_for('home'), 301)

	if request.method =="GET":
		return render_template('Signup.html',info=info, pg_name="Sign Up")


@site.route('/signin/', methods=['POST', 'GET'])
def signin():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	ParseInfo()

	if request.method =="POST":
		global login_s_error
		RememberMe = request.form.get("RememberMe_signin")
		if RememberMe == ("on"):
			RememberMe = True
		elif RememberMe == (None):
			RememberMe = False
		form_data = request.form
		signin_user = sUser(form_data['username_signin'], form_data['password_signin'])
		signin_user.user_login()
		if signin_user.error != None:
			print (signin_user.error)
			login_s_error = signin_user.error
			return redirect(url_for('error'), 302)
		if signin_user.success_login == True:
			login_user(signin_user.current_user_login, remember=RememberMe)
			print ("User successfully signed in")
			return redirect(url_for('home'), 302)

	if request.method =="GET":
		return render_template('Signin.html',info=info, pg_name="Sign In")


@site.route('/logout/')
@site.route('/signout/')
def signout():
	logout_user()
	return redirect(url_for('home'))


@site.route('/about')
def about():
	ParseInfo()
	return render_template('About.html')

@site.route('/shutdownserver1034')
def shutdown():
    shutdown_server()
    return redirect(url_for('home'))


@site.route('/purgekey')
def purgekey():
	purge = sk()
	purge.purgeKey()
	return redirect(url_for('shutdown'))


@site.route('/error/')
def error():
	ParseInfo()
	return render_template('Error.html',info=info, pg_name="Error", ErMsg=login_s_error)



#Importing dependencies and modules
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, current_user, logout_user
from ATS import site, db, mail
#custom made modules
from ATS.models import User, Item, Order
from ATS.register_to_db import rUser, vUser
from ATS.login_from_db import sUser
from ATS.skHandler import sk
from ATS.user_verification import CheckVerifyToken
from ATS import getInfo as getInfo

getInfo.RunGetInfo()

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    func()

def ParseInfo():
#purpose of function is to put all the information that a template requires 
	global info
	try:
		if current_user.YGS:
			if current_user.YGS != "S":
				user_type = ("Student")
			else:
				user_type = ("Staff")
	except:
		user_type = ("Guest")
	try:
		username = current_user.Username
		fullname = (current_user.First_name + " " + current_user.Last_name)
	except:
		username = None
		fullname = None
	print (f"request by {username}")

	page_title = (user_type + ": ")
	getInfo.RunGetInfo()
	info = {
		'page_title': (page_title),
		'date' :(getInfo.date),
		'day': (getInfo.day),
		'TimeOfDay': (getInfo.TimeOfDay),
		'AccademicYear12': (getInfo.StartYear12),
		'AccademicYear13': (getInfo.StartYear13),
		'Current_Username': (username),
		'Current_Fullname': (fullname)
	}


#The routes below are used for user authentication and similar processes

@site.route('/signup/', methods=['POST', 'GET'])
#many people tend to go to /signup to try to register, this redirects them to the /register page
def gotoregister():
	return redirect(url_for('register'), 301)

@site.route('/register/', methods=['POST', 'GET'])
def register():
	#lets the user register to the system
	if current_user.is_authenticated:
		return redirect(url_for('home'))
		flash("You already have an account", 'warning')
	ParseInfo()

	if request.method == 'POST':
		global site_error
		form_data = request.form
		new_user = rUser(form_data['First_Name_Form'], form_data['Last_Name_Form'], form_data['Forest_Username_Form'], form_data['Forest_Email_Domain_Form'], form_data['AccademicYear_Form'], form_data['House_Form'], form_data['Password_Form'])
		new_user.add_new_user()
		#Checks if any errors were produced
		if new_user.error != None:
			print (new_user.error)
			site_error = new_user.error
			flash(site_error, 'danger')
			return render_template('Signup.html',info=info, pg_name="Sign Up")
		flash("Email has been sent to your @forest email. Please verify your account before signing in. If account not verified within 7 days, username will be marked as spam and not be allowed to resignup", 'info')
		return redirect(url_for('home'), 301)
	if request.method =="GET":
		return render_template('Signup.html',info=info, pg_name="Sign Up")

@site.route('/signin/', methods=['POST', 'GET'])
def signin():
	#Lets the user sign in
	if current_user.is_authenticated:
		flash("You already have signed in", 'warning')
		return redirect(url_for('home'))
	ParseInfo()

	if request.method =="POST":
		global site_error
		RememberMe = request.form.get("RememberMe_signin")
		if RememberMe == ("on"):
			RememberMe = True
		elif RememberMe == (None):
			RememberMe = False
		form_data = request.form
		signin_user = sUser(form_data['username_signin'], form_data['password_signin'])
		signin_user.user_login()
		if signin_user.error != None:
			#Checks if any errors were produced
			print (signin_user.error)
			site_error = signin_user.error
			flash(site_error, 'danger')
			return render_template('Signin.html',info=info, pg_name="Sign In")
		if signin_user.success_login == True:
			login_user(signin_user.current_user_login, remember=RememberMe)
			flash("Successfully signed in", 'success')
			print("User signed in")
			return redirect(url_for('home'), 302)
	if request.method =="GET":
		return render_template('Signin.html',info=info, pg_name="Sign In")

@site.route('/logout/')
@site.route('/signout/')
#Signs out the user
def signout():
	logout_user()
	flash("You've signed out", 'info')
	return redirect(url_for('home'))

@site.route('/verify_manual/', methods=['POST', 'GET'])
#Incase the automatic link does not work, this will allow users to verify their accounts
def verify_manual():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	ParseInfo()

	if request.method =="POST":
		global site_error
		form_data = request.form
		verify_user = CheckVerifyToken(form_data['username_verify'], form_data['token_verify'])
		status = verify_user.check_verify_token()
		if status != ("Verified"):
			site_error = verify_user.error
			flash(site_error, 'danger')
			return render_template('AccountVerify.html',info=info, pg_name="Verify Your Account")
		elif status == ("Verified"):
			verifying_user = vUser(form_data['username_verify'])
			verifying_user.verify_user()
			flash("Your account has been verified!", 'success')
			return redirect(url_for('home'))

	if request.method =="GET":
		return render_template('AccountVerify.html',info=info, pg_name="Verify Your Account")

@site.route('/verify_auto/<vUsername>/<vToken>/')
#This link automatically verifies an account if it is still valid
def verify_auto(vUsername,vToken):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	ParseInfo()

	global site_error
	verify_user = CheckVerifyToken(vUsername, vToken)
	status = verify_user.check_verify_token()
	if status != ("Verified"):
		site_error = verify_user.error
		flash(site_error, 'danger')
		return redirect(url_for('verify_manual'))
	elif status == ("Verified"):
		verifying_user = vUser(vUsername)
		verifying_user.verify_user()
		flash("Your account has been verified!", 'success')
		return redirect(url_for('home'))

#End of user authentication section

#These routes are for general pages
@site.route('/home')
@site.route('/')
def home():
	ParseInfo()
	return render_template('Home.html',info=info, pg_name="Home", sidebar="yes")


@site.route('/about')
def about():
	ParseInfo()
	return render_template('About.html')






#Admin routes used for system maintainance
def admin_perm_check():
	if current_user.is_authenticated:
		if current_user.Admin_status == (1):
			return True
	return False



@site.route('/restart_server')
def shutdown():
	admin = admin_perm_check()
	if admin == True:
		shutdown_server()
		flash (f"Server Restart inititiated by {current_user.Username}", warning)
	else:
		flash("Whoops! Looks like you don't have permission to do that! If you think this is a mistake, please contact support", "danger")
	return redirect(url_for('home'))




@site.route('/purgekey')
def purgekey():
	purge = sk()
	purge.purgeKey()
	return redirect(url_for('shutdown'))




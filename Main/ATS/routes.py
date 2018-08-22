from flask import render_template, url_for, request, redirect
from ATS import site

from ATS.models import User, Item, Order
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

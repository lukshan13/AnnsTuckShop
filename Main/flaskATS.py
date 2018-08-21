print ("Developed By Lukshan Sharvaswaran, DvDt:2018. @lukshan13")

#calling in required libraries for code
import flask
from flask import Flask, render_template, url_for, request, redirect
import getInfo as getInfo
import os



site = Flask(__name__)
#hardcoding values incase no values are returned from database to prevent errors
userType = ("nil")
page = ("nil")


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
		Last_Name = request.form.get('Last_Name_Form')
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



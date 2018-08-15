print ("Developed By Lukshan Sharvaswaran, DvDt:2018. @lukshan13")

#calling in required libraries for code
import flask
from flask import Flask, render_template, url_for, request
import getInfo as getInfo
import os

site = Flask(__name__)
#hardcoding values incase no values are returned from database to prevent errors
userType = ("nil")
page = ("nil")


#from getInfo 
getInfo.RunGetInfo()
'''TEMP'''
userType = ("Student")
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
		'AccademicYear12': (getInfo.year12),
		'AccademicYear13': (getInfo.year13)
	}

@site.route('/home')
@site.route('/')
def home():
	ParseInfo()
	return render_template('Home.html',info=info, pg_name="Home", sidebar="yes")

@site.route('/signup/')
@site.route('/register/')
def register():
	ParseInfo()
	return render_template('signup.html',info=info, pg_name="Sign Up")

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



print ("Developed By Lukshan Sharvaswaran, DvDt:2018. @lukshan13")

#calling in required libraries for code
import flask
from flask import Flask, render_template, url_for
import getInfo as getInfo

site = Flask(__name__)
#hardcoding values incase no values are returned from database to prevent errors
userType = ("nil")
page = ("nil")



#from getInfo 
getInfo.get_datetime(), getInfo.get_TimeOfDay()
'''TEMP'''
userType = ("Student")
page_title = (userType + ": ")




info = {
	'page_title': (page_title),
	'date' :(getInfo.date),
	'day': (getInfo.day),
	'TimeOfDay': (getInfo.TimeOfDay)
}

@site.route('/home')
@site.route('/')
def home():
    return render_template('Home.html',info=info, pg_name="Home", sidebar="yes")

@site.route('/signup/')
@site.route('/register/')
def signip():
	return render_template('signup.html',info=info, pg_name="Sign Up")

@site.route('/about')
def about():
	return render_template('About.html')

#enabling debug mode when execured via terminal
if __name__ == '__main__':
	site.run(debug=True)

print (getInfo.TimeOfDay, "'Ann's Tuck Shop' site flask server is now running. Please navigate to the address below to access the site.")



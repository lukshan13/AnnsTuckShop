#fetching date and time
import datetime
import time

def get_datetime():
    global now, date, day, ctime, time_mins, time_display
    now = datetime.datetime.now()
    date = (now.strftime("%B %d, %Y"))
    day = (now.strftime("%A"))
    ctime = (time.localtime()[3], time.localtime()[4])
    time_display = (str(ctime[0])) + ":" + (str(ctime[1]))
    time_mins = (ctime[0]*60)+(ctime[1])
    

def get_TimeOfDay():
	global TimeOfDay
	if time_mins >= (1021):
	    TimeOfDay = ("Good Evening!")
	elif (721) <= time_mins <= (1020)  :
	    TimeOfDay = ("Good Afternoon!")
	elif time_mins <= (720):
	    TimeOfDay = ("Good Morning!")
	else:
	    TimeOfDay = ("Hello!")

def get_AccademicYear():
	global year12, year13
	if (now.month) <= (7):
		year12 = (now.year - 1)
		year13 = (year12-1)
	else:
		year12 = (now.year)
		year13 = (year12 -1)
	



def RunGetInfo():
	get_datetime()
	get_TimeOfDay()
	get_AccademicYear()
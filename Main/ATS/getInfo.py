#getinfo.py

#fetching date and time
from ATS.models import BreakfastTimetable, QuarterTimetable, Item
import datetime
import time

#This module is designed to get most of the basic data that is reqired by the applications, such as date, time, current options, ect.

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
	    TimeOfDay = ("Evening")
	elif (721) <= time_mins <= (1020)  :
	    TimeOfDay = ("Afternoon")
	elif time_mins <= (720):
	    TimeOfDay = ("Morning")
	else:
	    TimeOfDay = ("Day")

def get_AccademicYear():
	global StartYear12, StartYear13
	if (now.month) <= (7):
		StartYear12 = (now.year - 1)
		StartYear13 = (StartYear12-1)
	else:
		StartYear12 = (now.year)
		StartYear13 = (StartYear12 -1)
	
def get_CurrentItems():
	try:
		global homeInfo
		breakfast_today = BreakfastTimetable.query.filter_by(Day=day).first()
		breakfast_item = Item.query.filter_by(id=breakfast_today.Breakfast_Item).first().Item_name

		quarter_today = QuarterTimetable.query.filter_by(Day=day).first()
		quarter_item = Item.query.filter_by(id=quarter_today.Quarter_Item).first().Item_name

		WeekSpecial = Item.query.filter_by(WeekSpecial=(1)).first()

		homeInfo = {
		"breakfast_item": breakfast_item,
		"quarter_item": quarter_item,
		"week_special": WeekSpecial
		}
	except:
		homeInfo = {
		"breakfast_item": "Unavailable",
		"quarter_item": "Unavailable"
		}

def RunGetInfo():
	get_datetime()
	get_TimeOfDay()
	get_AccademicYear()
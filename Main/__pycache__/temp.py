import datetime
import time

#def get_date():
#	global date
#	global day
#	now = datetime.datetime.now()
#	date = (now.strftime("%B %d, %Y"))
#	day = (now.strftime("%A"))

global date, day, time, time_mins
now = datetime.datetime.now
date = (now.strftime("%B %d, %Y"))
day = (now.strftime("%A"))
time = (time.localtime()[3], time.localtime()[4])
time_mins = (time[0]*60)+(time[1])


class Time_date:

	cdate = None
	cday = None
	ctime = None
	

	def __init__(self, cdate, cday, ctime):
		self.cdate = date
		self.cday = day
		self.ctime = time
  
      def say_e(self):
          print (time)

	
     
          

dt = Time_date(date,day,time)


dt.say_e()
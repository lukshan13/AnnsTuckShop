from ATS import db
from ATS.models import BreakfastTimetable, QuarterTimetable, Item, Order
import getInfo as getInfo


class BreakfastOptions:

	def getInfoFromDB(self):
		today = getInfo.day.lower()
		print (today)
		breakfast_today = BreakfastTimetable.query
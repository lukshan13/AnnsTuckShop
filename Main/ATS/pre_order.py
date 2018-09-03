from ATS import db
from ATS.models import BreakfastTimetable, QuarterTimetable, Item, Order
import getInfo as getInfo


class BreakfastOptions:

	def getInfoFromDB(self):
		today = 
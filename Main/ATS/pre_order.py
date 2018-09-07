from ATS import db
from sqlalchemy import and_
from ATS.models import BreakfastTimetable, QuarterTimetable, Item, Order
from ATS import getInfo as getInfo


class PreOrderOptions:

	def __init__(self, id, mode):
		self.UserID = id
		if mode == "breakfast":
			self.today = getInfo.day
			breakfast_today = BreakfastTimetable.query.filter_by(Day=self.today).first()
			

			self._today_id = breakfast_today.Breakfast_Item
			self.current_item = Item.query.filter_by(id=self._today_id).first()
			self.Time = "Breakfast"

		elif mode == "quarter":
			self.today = getInfo.day
			quarter_today = QuarterTimetable.query.filter_by(Day=self.today).first()
			

			self._today_id = quarter_today.Quarter_Item
			self.current_item = Item.query.filter_by(id=self._today_id).first()
			self.Time = "Quarter"



	def getInfoFromDB(self):
		(self.current_item.Price) = str(self.current_item.Price)
		self.current_item.Price = "£" + self.current_item.Price[:-2] + "." + self.current_item.Price[-2:]
		#print (priceReform)
		self.data = {
		"current_Item": self.current_item.Item_name,
		"price": self.current_item.Price,
		"time_for": self.Time,
		"day": self.today
		}
		print (self.data)

	def checkForPreorder(self):
		check = Order.query.filter(and_(Order.User_id==self.UserID), (Order.Order_Item==self._today_id)).first()
		if check != None and check.Current == 1:
			print (check)	
			return True
		else:
			return False


	def run(self):
		self.getInfoFromDB()
		return self.checkForPreorder()


class SubmitePreorder:

	def __init__(self, id):
		userId = id
			

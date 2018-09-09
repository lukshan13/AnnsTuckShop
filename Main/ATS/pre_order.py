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
		print(self.current_item.Price)
		self.Price = "£" + self.current_item.Price[:-2] + "." + self.current_item.Price[-2:]
		#print (priceReform)
		self.data = {
		"current_Item": self.current_item.Item_name,
		"current_Item_id": self.current_item.id,
		"price": self.Price,
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


class SubmitPreorder:

	def __init__(self, user_id, order_item, time_for, day_for):
		self.userId = user_id
		self.order_item = order_item
		self.time_for = time_for
		self.day_for = day_for
	
	
	def submit(self):
		try:
			new_order = Order(User_id=self.userId, Order_Item=self.order_item, Date_for=self.day_for, Time_for=self.time_for, Current=1)
			db.session.add(new_order)
			db.session.commit()
		except:
			return "Something has gone wrong. Please try again later."


class UserPreorders:

	def __init__(self, user):
		try:
			OrderID = []
			Item_name = []
			ItemPrice = []
			Collected = []
			TimeFor = []
			Data = Order.query.filter_by(User_id=user).all()
			Count = []
			counter = 0
			self.OrderData = None
			for items in Data:
				order = (Order.query.filter_by(id=(items.id)).first())
				item = (Item.query.filter_by(id=(order.Order_Item)).first())
				OrderID.append(order.id)
				Item_name.append(item.Item_name)
				ItemPrice.append(item.Price)
				TimeFor.append(order.Time_for)
				if order.Current == 1:
					Collected.append("No")
				elif order.Current == 0:
					Collected.append("Yes")
				Count.append(counter)
				self.OrderData = {
				"Count": Count,
				"OrderID": OrderID,
				"Item_name": Item_name,
				"ItemPrice": ItemPrice,
				"TimeFor": TimeFor,
				"Collected": Collected
				}
				counter = counter+1
			print(self.OrderData)
		except:
			pass
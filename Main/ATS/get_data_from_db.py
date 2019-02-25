#get_data_from_db.py

from ATS import db
from ATS import getInfo as getInfo
from ATS.models import BreakfastTimetable, QuarterTimetable, Item, Order, User

class TableGetter:

	tableData = None
	OrderData = None

	def breakfast_table_get(self):
		self.Breakfast_List = []
		for i in range(7):
			i=i+1
			current_id = BreakfastTimetable.query.filter_by(id=(i)).first()
			current_foodItem = Item.query.filter_by(id=current_id.Breakfast_Item).first()
			self.Breakfast_List.append(current_foodItem.Item_name)

	def quarter_table_get(self):
		self.Quarter_List = []
		for i in range(7):
			i=i+1
			current_id = QuarterTimetable.query.filter_by(id=(i)).first()
			current_foodItem = Item.query.filter_by(id=current_id.Quarter_Item).first()
			self.Quarter_List.append(current_foodItem.Item_name)


	def getQBTables(self):
		self.breakfast_table_get()
		self.quarter_table_get()
		self.tableData = {
		'Breakfast': self.Breakfast_List,
		'Quarter': self.Quarter_List
		}


	def getPre_orders(self):
		OrderID = []
		Item_name = []
		ItemPrice = []
		UserName = []
		Year = []
		TimeFor = []
		Data = Order.query.all()
		Count = []
		counter = 0
		#recursive algorithm that puts data in lists, and then places the lists in a dict
		for items in Data:
			if items.Current == 1:
				order = (Order.query.filter_by(id=(items.id)).first())
				item = (Item.query.filter_by(id=(order.Order_Item)).first())
				user = (User.query.filter_by(id=(order.User_id)).first())
				OrderID.append(order.id)
				Item_name.append(item.Item_name)
				ItemPrice.append(item.Price)
				FullName = (f"{user.First_name}.{(user.Last_name)[:1]}")
				UserName.append(FullName)
				Year.append(user.YGS)
				TimeFor.append(order.Time_for)
				Count.append(counter)
				self.OrderData = {
				"Count": Count,
				"OrderID": OrderID,
				"Item_name": Item_name,
				"ItemPrice": ItemPrice,
				"UserName": UserName,
				"Year": Year,
				"TimeFor": TimeFor
				}
				counter = counter+1

	#Clears order history
	def Log_and_ClearAll(self):
		self.orders = (Order.query.all())
		self.file_open_and_log()
		for order_ in self.orders:
			Order.query.filter_by(id=order_.id).delete()
			db.session.commit()

	#Stores order history in a txt file,
	def file_open_and_log(self):
		getInfo.get_datetime()
		with open("ATS/static/OrderLog.txt","a+") as OrderLog:
			OrderLog.write("\nOrder logged and cleared - " + getInfo.day + " " + getInfo.date + " AT "+ getInfo.time_display +"\n")
			for order_ in self.orders:
				item = Item.query.filter_by(id=order_.Order_Item).first()
				info = f" {item.Item_name} bought for {order_.Time_for}. Order ID: {order_.id}. Ordered by UserID: {order_.User_id}. \tOrder Collected: {order_.Current} \n"
				OrderLog.write(str(info))

	#Adds complete status to an order
	def completePre_Orders(self, completedID):
		if completedID == "all":
			self.Log_and_ClearAll()
			return
		order = (Order.query.filter_by(id=(completedID)).first())
		order.Current = (0)
		db.session.commit()
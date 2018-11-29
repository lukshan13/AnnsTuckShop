from ATS import db
from ATS.models import User, Item, Order, QuarterTimetable, BreakfastTimetable


#Shop options
class Admin_Add_Item:

	def __init__(self, name, Type, price):
		self.itemName = name
		self.itemPrice = price
		self.itemType = Type


	def check_existing(self):
		if Item.query.filter_by(Item_name=self.itemName).first() == None:
			return True
		else:
			return False

	def add_to_db(self):
		newItem = Item(Item_name=self.itemName, Type=self.itemType, Price=self.itemPrice)
		db.session.add(newItem)
		db.session.commit()
		print ("committed")

	def add_item(self):
		if self.check_existing() == True:
			self.add_to_db()
			return False
		else:
			return True


class Admin_Delete_Item:
	def __init__(self, delkey):
		if delkey == "view":
			self.GetItems()
		else:
			self.key = delkey
			self.DeleteItem()


	def GetItems(self):
		item_name = []
		ItemPrice = []
		Id = []
		Editable = []
		Count = []
		items = Item.query.all()
		counter = 1
		for item in items:
			if item.inQuarterTimetable or item.inBreakfastTimetable:
				Editable.append(0)
			else:
				Editable.append(1)
			Count.append(counter)
			counter = counter+1
			item_name.append(item.Item_name)
			ItemPrice.append(item.Price)
			Id.append(item.id)
		self.itemData = {
		"Count": Count,
		"ItemID": Id,
		"Item_name": item_name,
		"ItemPrice": ItemPrice,
		"Editable": Editable
		}

	def DeleteItem(self):
		dItem = Item.query.filter_by(id=self.key).delete()
		db.session.commit()


class Admin_Modify_Table:

	def __init__(self, table, mode, data=None):
		if table == "breakfast":
			self.tableData = BreakfastTimetable.query.all()
		elif table == "quarter":
			self.tableData = QuarterTimetable.query.all()
		elif table == "week-special":
			self.tableData = Item.query.filter_by(WeekSpecial="1").first()
		if mode == "view":
			self.view_table(table)
		elif mode == "view-week-special":
			self.view_week_special()
		elif mode == "modify-week-special":
			self.change_week_special(data)
		elif mode != "view":
			self.change_table(table, mode)

	def view_table(self, table):
		items = Item.query.all()
		Items = []
		for item in items:
			Items.append(item.Item_name)
		Day = []
		item_name = []
		counter = []
		count = 0
		for entry in self.tableData:
			Day.append(entry.Day)
			if table == "breakfast":
				item_name.append((Item.query.filter_by(id=entry.Breakfast_Item).first().Item_name))			
			elif table == "quarter":
				item_name.append((Item.query.filter_by(id=entry.Quarter_Item).first().Item_name))
			counter.append(count)
			count = count + 1			
		self.tableExport = {
		"count": counter,
		"day": Day,
		"item_name": item_name,
		"allItems": Items
		}

	def view_week_special(self):
		Items = []
		items = Item.query.all()
		for item in items:
			Items.append(item.Item_name)
		if self.tableData == None:
			self.weekSpecial = {"ItemName": "None", "ItemPrice": "N/A", "allItems": Items}
		else:
			self.weekSpecial = {"ItemName": self.tableData.Item_name, "ItemPrice": self.tableData.Price, "allItems": Items}

	def change_table(self, table, data):
		for entry in data:
			if data[entry] != "ignore" and entry != "csrf_token":
				if table == "breakfast":
					toModify = BreakfastTimetable.query.filter_by(Day=entry).first()
					toModify.Breakfast_Item=(Item.query.filter_by(Item_name=data[entry]).first().id)
				elif table == "quarter":
					toModify = QuarterTimetable.query.filter_by(Day=entry).first()
					toModify.Quarter_Item=(Item.query.filter_by(Item_name=data[entry]).first().id)
				db.session.commit()

	def change_week_special(self, data):
		if (data["NewItem"]) != "ignore":
			oldItem = Item.query.filter_by(WeekSpecial="1").first()
			if oldItem != None:
				oldItem.WeekSpecial = None
			newItem = Item.query.filter_by(Item_name=data["NewItem"]).first()
			newItem.WeekSpecial = (1)
			db.session.commit()			



#Account options



class Admin_View_Delete_Account:

	def __init__(self, mode, user):
		if mode == "view":
			self.view_users()
		elif mode == "delete":
			self.deleteUser(user)

	def view_users(self):
		first_name = []
		last_name = []
		username = []
		ygs = []
		house = []
		counter = []
		admin = []
		count = 0
		users = User.query.all()
		for user in users:
			if user.id == (0):
				continue
			first_name.append(user.First_name)
			last_name.append(user.Last_name)
			username.append(user.Username)
			ygs.append(user.YGS)
			house.append(user.House)
			counter.append(count)
			admin.append(user.Admin_status)
			count = count + 1
		self.allUsersData = {
		"FirstName": first_name,
		"LastName": last_name,
		"Username": username,
		"YGS": ygs,
		"House": house,
		"AdminState": admin,
		"Count": counter
		}


	def deleteUser(self, username):
		dUser = User.query.filter_by(Username=username).delete()
		db.session.commit()

class Admin_Verify_Account:
	
	def viewUnverified(self):

		users = User.query.all()
		first_name = []
		last_name = []
		username = []
		ygs = []
		house = []
		counter = []
		count = 0
		users = User.query.all()
		for user in users:
			if user.AccVerified == (0):
				first_name.append(user.First_name)
				last_name.append(user.Last_name)
				username.append(user.Username)
				ygs.append(user.YGS)
				house.append(user.House)
				counter.append(count)
				count = count + 1
		self.UnverifiedUsersData = {
		"FirstName": first_name,
		"LastName": last_name,
		"Username": username,
		"YGS": ygs,
		"House": house,
		"Count": counter
		}


	def verifyUser(self, username):
		user = User.query.filter_by(Username=username).first()
		user.AccVerified = (1)
		db.session.commit()
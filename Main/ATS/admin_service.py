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

	def __init__(self, table, mode):
		if table == "breakfast":
			self.tableData = BreakfastTimetable.query.all()
		elif table == "quarter":
			self.tableData = QuarterTimetable.query.all()
		if mode == "view":
			self.view_table(table)
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

	def change_table(self, table, data):
		for entry in data:
			if data[entry] != "ignore":
				if table == "breakfast":
					toModify = BreakfastTimetable.query.filter_by(Day=entry).first()
					toModify.Breakfast_Item=(Item.query.filter_by(Item_name=data[entry]).first().id)
				elif table == "quarter":
					toModify = QuarterTimetable.query.filter_by(Day=entry).first()
					toModify.Quarter_Item=(Item.query.filter_by(Item_name=data[entry]).first().id)
				print (toModify)
				db.session.commit()


class Admin_Modify_Week_Special:
	pass



#Account options

class Admin_Add_New_Account:
	pass

class Admin_Delete_Account:
	pass

class Admin_Verify_Account:
	pass

class Admin_View_and_Modify_Account:
	pass



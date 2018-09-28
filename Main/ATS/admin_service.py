from ATS import db
from ATS.models import User, Item, Order, QuarterTimetable, BreakfastTimetable


#Shop options
class Admin_Add_Item:

	def __init__(self, name, price, Type):
		self.itemName = name
		self.itemPrice = price
		self.itemType = Type

	def check_existing(self):
		if Item.query.filter_by(Item_name=self.itemName).first() != None:
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
	pass

class Admin_Modify_Table:

	def __init__(self, table):
		pass

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



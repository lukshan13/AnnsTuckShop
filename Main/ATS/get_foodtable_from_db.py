from ATS import db
from ATS.models import BreakfastTimetable, QuarterTimetable, Item

class TableGetter:

	Breakfast_List = []
	Quarter_List = []
	tableData = None

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


	def getTables(self):
		self.breakfast_table_get()
		self.quarter_table_get()
		self.tableData = {
		'Breakfast': self.Breakfast_List,
		'Quarter': self.Quarter_List
		}
		print (self.tableData)




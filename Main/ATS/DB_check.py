from ATS import db
from ATS.models import BreakfastTimetable, QuarterTimetable, User, Order, Item
from ATS.passwordManager import passwordHash


class check_item_null:
	pass


class check_default_entries:

	def check_admin(self):
		defaultUser = User.query.filter_by(id=0).first()
		if not defaultUser:
			hashpassword = passwordHash()
			hashpass = hashpassword.hashPassword_RandomSalt("tuck18")
			defaultAdmin = User(id= (0), First_name="ATS", Last_name="SFC", Username="ATS", Year="S", Email="ATS@forest.org.uk", House="Astell", Password=hashpass["password"], Salt=hashpass["salt"], HashVer=hashpass["algorithmVer"], AccVerified="1", Admin_status="1")
			print ("DB has been updated.")
			db.session.add(defaultAdmin)
			db.session.commit()

	def check_none_item(self):
		noneItem = Item.query.filter_by(id=0).first()
		if not noneItem:
			defaultNoneItem = Item(id = (0), Item_name = "None", Type= "None", Price = (0))
			print ("DB has been updated.")
			db.session.add(defaultNoneItem)
			db.session.commit()




class check_breakfast:

	breakfast_table = None
	count = None

	def check_no_extra(self):
		self.breakfast_table = BreakfastTimetable.query.all()
		self.count = 0
		try:
			Last = BreakfastTimetable.query.filter_by(id=(7)).first()
			if Last.Day != "Sunday":
				return
		except(AttributeError):
			return
		for item in self.breakfast_table:
			Daybank = [None, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
			#if item.Day == "Monday" or item.Day == "Tuesday" or item.Day == "Wednesday" or item.Day == "Thursday" or item.Day == "Friday" or item.Day == "Saturday" or item.Day == "Sunday":
			if item.Day in Daybank:
				self.count = self.count+1
			else:
				print ("InValid Entry:", item)
				print ("Warning: Invalid entry detected: Deleting Invalid entry")
				BreakfastTimetable.query.filter_by(id=item.id).delete()
				db.session.commit()

	def refresh_days(self):
		Daybank = [None, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
		for i in range(7):
			i = i+1
			current_t =BreakfastTimetable.query.filter_by(id=i).first()
			try:
				print (current_t.Day)
				if current_t.Day == Daybank[i]:
					print (True)
				else:
					raise AttributeError
			except(AttributeError):
				print ("Error: Data Missing or Corrupted for", Daybank[i], ", Rebuilding...")

				BreakfastTimetable.query.filter_by(id=i).delete()
				BreakfastTimetable.query.filter_by(Day=Daybank[i]).delete()
				dayData = BreakfastTimetable(id=(i), Day=Daybank[i], Breakfast_Item=(0))
				db.session.add(dayData)
				db.session.commit()

	def checkBreakfast(self):
		self.check_no_extra()
		if self.count < 7:
			print ("Missing data detected!! Running diagnostics")
			self.refresh_days()
			self.checkBreakfast()





class check_quarter:

	quarter_table = None
	count = None

	def check_no_extra(self):
		self.quarter_table = QuarterTimetable.query.all()
		self.count = 0
		Last = BreakfastTimetable.query.filter_by(id=(7)).first()
		if Last.Day != "Sunday":
			return
		for item in self.quarter_table:
			Daybank = [None, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
			if item.Day in Daybank:
				self.count = self.count+1
			else:
				print ("InValid Entry:", item)
				print ("Warning: Invalid entry detected: Deleteing Invalid entry")
				QuarterTimetable.query.filter_by(id=item.id).delete()
				db.session.commit()

	def refresh_days(self):
		Daybank = [None, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
		for i in range(7):
			i = i+1
			current_t =QuarterTimetable.query.filter_by(id=i).first()
			try:
				print (current_t.Day)
				if current_t.Day == Daybank[i]:
					print (True)
				else:
					raise AttributeError
			except(AttributeError):
				print ("Error: Data Missing or Corrupted for", Daybank[i], ", Rebuilding...")

				QuarterTimetable.query.filter_by(id=i).delete()
				QuarterTimetable.query.filter_by(Day=Daybank[i]).delete()
				dayData = QuarterTimetable(id=(i), Day=Daybank[i], Quarter_Item=(0))
				db.session.add(dayData)
				db.session.commit()

	def checkQuarter(self):
		self.check_no_extra()
		if self.count < 7:
			print ("Missing data detected!! Running diagnostics")
			self.refresh_days()
			self.checkQuarter()

from ATS import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	First_name = db.Column(db.String(25), unique=True, nullable=False)
	Last_name = db.Column(db.String(25), unique=True, nullable=False)
	Username = db.Column(db.String(25), unique=True, nullable=False)
	YGS = db.Column(db.String(7), nullable=False)
	Email = db.Column(db.String(120), unique=True, nullable=False)
	House = db.Column(db.String(10), nullable=False)
	Password = db.Column(db.String(120), nullable=False)
	AccVerified = db.Column(db.Integer, nullable=False, default=0)
	Admin_status = db.Column(db.Integer, nullable=False, default=0)
	Orders = db.relationship('Order', backref=('customer'), lazy=True)


	def __repr__(self):
		return f"User('{self.First_name}', '{self.Last_name}', '{self.Username}', '{self.House}')"


class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	Item_name = db.Column(db.String(25), unique=True, nullable=False)
	Type = db.Column(db.String(8), nullable=False)
	Price = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"User('{self.id}', '{self.Item_name}', '{self.Type}', '{self.Price}')"


class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	User_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	Order_Item = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
	Date_for = db.Column(db.Integer, nullable=False)
	Time_for = db.Column(db.Integer, nullable=False)
	Current = db.Column(db.Integer, default=0, nullable=False)

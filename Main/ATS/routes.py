
#Importing dependencies and modules
from flask import render_template, url_for, request, redirect, flash, abort
from flask_login import login_user, current_user, logout_user
from ATS import site, db, mail
#custom made modules
from ATS.models import User, Item, Order
from ATS.register_to_db import rUser, vUser
from ATS.login_from_db import sUser
from ATS.skHandler import sk
from ATS.user_verification import CheckVerifyToken
from ATS.get_data_from_db import TableGetter
from ATS.pre_order import PreOrderOptions, SubmitPreorder, UserPreorders
from ATS import getInfo as getInfo
from ATS.admin_service import Admin_Add_Item, Admin_Delete_Item

getInfo.RunGetInfo()

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    func()

def ParseInfo():
#purpose of function is to put all the information that a template requires 
	global info
	try:
		if current_user.YGS:
			if current_user.YGS != "S":
				user_type = ("Student")
			else:
				user_type = ("Staff")
	except:
		user_type = ("Guest")
	try:
		username = current_user.Username
		fullname = (current_user.First_name + " " + current_user.Last_name)
	except:
		username = None
		fullname = None
	print (f"request by {username}")

	page_title = (user_type + ": ")
	getInfo.RunGetInfo()
	info = {
		'page_title': (page_title),
		'date' :(getInfo.date),
		'day': (getInfo.day),
		'TimeOfDay': (getInfo.TimeOfDay),
		'AccademicYear12': (getInfo.StartYear12),
		'AccademicYear13': (getInfo.StartYear13),
		'Current_Username': (username),
		'Current_Fullname': (fullname)
	}

@site.route('/lunch_menu')
def lunch_menu():
	return redirect("https://goo.gl/fCejpy")

#The routes below are used for user authentication and similar processes

@site.route('/signup/', methods=['POST', 'GET'])
#many people tend to go to /signup to try to register, this redirects them to the /register page
def gotoregister():
	return redirect(url_for('register'), 301)

@site.route('/register/', methods=['POST', 'GET'])
def register():
	#lets the user register to the system
	if current_user.is_authenticated:
		flash("You already have an account", 'warning')
		return redirect(url_for('home'))
	ParseInfo()

	if request.method == 'POST':
		global site_error
		form_data = request.form
		new_user = rUser(form_data['First_Name_Form'], form_data['Last_Name_Form'], form_data['Forest_Username_Form'], form_data['Forest_Email_Domain_Form'], form_data['AccademicYear_Form'], form_data['House_Form'], form_data['Password_Form'], 0)
		new_user.add_new_user()
		#Checks if any errors were produced
		if new_user.error != None:
			print (new_user.error)
			site_error = new_user.error
			flash(site_error, 'danger')
			return render_template('Signup.html',info=info, pg_name="Sign Up")
		flash("Email has been sent to your @forest email. Please verify your account before signing in. If account not verified within 7 days, username will be marked as spam and not be allowed to resignup. IF YOU CAN'T SEE THE EMAIL, PLEASE CHECK THAT IT HAS NOT BEEN SENT TO YOUR JUNK INBOX!", 'info')
		logout_user()
		return redirect(url_for('home'), 301)
	if request.method =="GET":
		flash("WARNING: Site is currently in private BETA. Email verification is disabled to allow private testing", "warning")
		return render_template('Signup.html',info=info, pg_name="Sign Up")


@site.route('/register/a/d/m/i/n/register', methods=['POST', 'GET'])
def register_admin():
	#lets the user register to the system as an admin (WARNING THIS SHOULD NOT BE REVEALED TO PUBLIC)
	if current_user.is_authenticated:
		flash("You already have an account", 'warning')
		return redirect(url_for('home'))
	ParseInfo()

	if request.method == 'POST':
		global site_error
		form_data = request.form
		new_user = rUser(form_data['First_Name_Form'], form_data['Last_Name_Form'], form_data['Forest_Username_Form'], form_data['Forest_Email_Domain_Form'], form_data['AccademicYear_Form'], form_data['House_Form'], form_data['Password_Form'], 1)
		new_user.add_new_user()
		#Checks if any errors were produced
		if new_user.error != None:
			print (new_user.error)
			site_error = new_user.error
			flash(site_error, 'danger')
			return render_template('Signup.html',info=info, pg_name="Sign Up")
		flash("Email has been sent to your @forest email. Please verify your account before signing in. If account not verified within 7 days, username will be marked as spam and not be allowed to resignup. If you can't see the email, please check that it has not been sent to your junk inbox!", 'info')
		logout_user()
		return redirect(url_for('home'), 301)
	if request.method =="GET":
		return render_template('Signup.html',info=info, pg_name="Sign Up")



@site.route('/signin/', methods=['POST', 'GET'])
def signin():
	#Lets the user sign in
	if current_user.is_authenticated:
		flash("You already have signed in", 'warning')
		return redirect(url_for('home'))
	ParseInfo()

	if request.method =="POST":
		global site_error
		RememberMe = request.form.get("RememberMe_signin")
		if RememberMe == ("on"):
			RememberMe = True
		elif RememberMe == (None):
			RememberMe = False
		form_data = request.form
		print ("login requested for", form_data['username_signin'])
		signin_user = sUser(form_data['username_signin'], form_data['password_signin'])
		signin_user.user_login()
		if signin_user.error != None:
			#Checks if any errors were produced
			print (signin_user.error)
			site_error = signin_user.error
			flash(site_error, 'danger')
			return render_template('Signin.html',info=info, pg_name="Sign In")
		if signin_user.success_login == True:
			login_user(signin_user.current_user_login, remember=RememberMe)
			flash("Successfully signed in", 'success')
			print("User signed in")
			return redirect(url_for('home'))
	if request.method =="GET":
		return render_template('Signin.html',info=info, pg_name="Sign In")

@site.route('/logout/')
@site.route('/signout/')
#Signs out the user
def signout():
	logout_user()
	flash("You've signed out", 'info')
	return redirect(url_for('home'))

@site.route('/verify_manual/', methods=['POST', 'GET'])
#Incase the automatic link does not work, this will allow users to verify their accounts
def verify_manual():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	ParseInfo()

	if request.method =="POST":
		global site_error
		form_data = request.form
		verify_user = CheckVerifyToken(form_data['username_verify'], form_data['token_verify'])
		status = verify_user.check_verify_token()
		if status != ("Verified"):
			site_error = verify_user.error
			flash(site_error, 'danger')
			return render_template('AccountVerify.html',info=info, pg_name="Verify Your Account")
		elif status == ("Verified"):
			verifying_user = vUser(form_data['username_verify'])
			verifying_user.verify_user()
			flash("Your account has been verified!", 'success')
			return redirect(url_for('home'))

	if request.method =="GET":
		return render_template('AccountVerify.html',info=info, pg_name="Verify Your Account")

@site.route('/verify_auto/<vUsername>/<vToken>/')
#This link automatically verifies an account if it is still valid
def verify_auto(vUsername,vToken):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	ParseInfo()

	global site_error
	verify_user = CheckVerifyToken(vUsername, vToken)
	status = verify_user.check_verify_token()
	if status != ("Verified"):
		site_error = verify_user.error
		flash(site_error, 'danger')
		return redirect(url_for('verify_manual'))
	elif status == ("Verified"):
		verifying_user = vUser(vUsername)
		verifying_user.verify_user()
		flash("Your account has been verified!", 'success')
		return redirect(url_for('home'))

#End of user authentication section

#These routes are for general pages
@site.route('/home')
@site.route('/')
def home():
	getInfo.get_CurrentItems()
	ParseInfo()
	return render_template('Home.html',info=info, pg_name="Home", sidebar="yes", homeInfo=getInfo.homeInfo)


@site.route('/pre-order/')
def redirect_pre_order():
	return redirect(url_for('pre_order', page="select"))
@site.route('/pre-order/<page>', methods=['POST', 'GET'])
def pre_order(page):
	ParseInfo()
	pg_name = "Pre-Order"

	if request.method =="POST":
		form_data = request.form
		check_Order = PreOrderOptions(current_user.id, (form_data["time_for"]).lower())
		if check_Order.run() != False:
			flash (check_Order.flashMessage,"danger")
			return redirect(url_for('food_table_none',))
		submit_order = SubmitPreorder(current_user.id, (form_data["item_id"]), (form_data["time_for"]), (form_data["day_for"]) )
		submit_order.submit()
		return redirect(url_for("home"))


	if page == "select":
		return render_template('preorder/Preorder-select.html',info=info, pg_name=pg_name, sidebar="yes")

	if page == "breakfast":
		if current_user.is_authenticated:
			bOrder = PreOrderOptions(current_user.id, "breakfast")
			if bOrder.run() != False: 
				flash (bOrder.flashMessage,"danger")
				return redirect(url_for('pre_order', page="my-orders"))
			else:
				return render_template('/preorder/Preorder-item.html',info=info, pg_name=pg_name, sidebar="yes", data=bOrder.data)
		else:
			flash ("Please log in to use this feature", "danger")
			return redirect(url_for('pre_order', page="select"))

	if page == "quarter":
		if current_user.is_authenticated:
			qOrder = PreOrderOptions(current_user.id, "quarter")
			if qOrder.run() != False: 
				flash (qOrder.flashMessage,"danger")
				return redirect(url_for('pre_order', page="my-orders"))
			else:
				return render_template('/preorder/Preorder-item.html',info=info, pg_name=pg_name, sidebar="yes", data=qOrder.data)
		else:
			flash ("Please log in to use this feature", "danger")
		return render_template('preorder/Preorder-select.html',info=info, pg_name=pg_name, sidebar="yes")

	if page == "my-orders":
		if current_user.is_authenticated:
			myOrders = UserPreorders(current_user.id)
			return render_template('preorder/Preorder-my-orders.html',info=info, pg_name=pg_name, sidebar="yes", OrderData=myOrders.OrderData)
		else:
			flash ("Please log in to use this feature", "danger")
			return redirect(url_for('pre_order', page="select"))


	return redirect(url_for('pre_order', page="select"))



@site.route('/shop')
def shop():
	ParseInfo()
	flash ("Whoops, this page is not complete yet! Hang tight, it'll be here soon!", "warning")
	return render_template('Home.html',info=info, pg_name="Home", sidebar="yes", homeInfo=getInfo.homeInfo)

@site.route('/balance-services')
def balance_services():
	ParseInfo()
	flash ("Whoops, this page is not complete yet! Hang tight, it'll be here soon!", "warning")
	return render_template('Home.html',info=info, pg_name="Home", sidebar="yes", homeInfo=getInfo.homeInfo)

@site.route('/account/')
def account():
	ParseInfo()
	if current_user.is_authenticated:
		flash ("Whoops, this page is not complete yet! Hang tight, it'll be here soon!", "warning")
		return render_template('/account/Account.html',info=info, pg_name="My Account", sidebar="yes")
	else:
		pass

@site.route('/account/edit/')
def edit_account_redirect():
	return redirect (url_for('edit_account', edit="select"))

@site.route('/account/edit/<edit>')
def edit_account(edit):
	ParseInfo()
	print (edit)
	if current_user.is_authenticated:
		return render_template('/account/Account.html',info=info, pg_name="My Account", sidebar="yes")
	else:
		flash ("Please log in to use this feature", "danger")
		return redirect(url_for("home"))


@site.route('/about')
def about():
	ParseInfo()
	return render_template('About.html')

@site.route('/table/<highlight>')
def food_table(highlight):
	ParseInfo()
	Table = TableGetter()
	Table.getQBTables()
	return render_template('/FoodTable.html', info=info, pg_name="FoodTable",sidebar="yes", highlight=highlight, table_data=Table.tableData)

@site.route('/table/')
def food_table_none():
	ParseInfo()
	Table = TableGetter()
	Table.getQBTables()
	return render_template('/FoodTable.html', info=info, pg_name="FoodTable",sidebar="yes", highlight="None", table_data=Table.tableData)




#-------------------------------------------------------------------------------------------------------------



#Admin routes used for system maintainance
def admin_perm_check():
	if current_user.is_authenticated:
		if current_user.Admin_status == (1):
			return True
		elif current_user.Admin_status != (1):
			return False
	return False




@site.route('/admin')
def adminpage():
	admin = admin_perm_check()
	ParseInfo()
	if admin == True:
		return render_template('/admin/Adminpage.html',info=info, pg_name="Admin", sidebar="no")
	else:
		flash("Whoops! Looks like you don't have permission to do that! If you think this is a mistake, please contact support", "danger")
		return redirect(url_for('home'))



@site.route('/admin/view-pre-orders')
def view_preorder():
	admin = admin_perm_check()
	ParseInfo()
	if admin == True:
		Table = TableGetter()
		Table.getPre_orders()
		return render_template('/admin/View_preorder.html',info=info, pg_name="Admin", sidebar="no", OrderData = Table.OrderData)
	else:
		flash("Whoops! Looks like you don't have permission to do that! If you think this is a mistake, please contact support", "danger")
		return redirect(url_for('home'))

@site.route('/admin/view-pre-orders/completed/<id>')
def complete_order(id):
	completeOrder = TableGetter()
	completeOrder.completePre_Orders(id)
	return redirect(request.referrer)



@site.route('/admin/add-new-user', methods=['POST', 'GET'])
def admin_add_new_user():
	ParseInfo()

	if request.method == 'POST':
		form_data = request.form
		print (form_data)
		new_user = rUser(form_data['First_Name_Form'], form_data['Last_Name_Form'], form_data['Forest_Username_Form'], form_data['Forest_Email_Domain_Form'], form_data['AccademicYear_Form'], form_data['House_Form'], form_data['Password_Form'], form_data['Admin_account'])
		new_user.admin_add_new_user()
		#Checks if any errors were produced
		if new_user.error != None:
			print (new_user.error)
			site_error = new_user.error
			flash(site_error, 'danger')
			return render_template('Signup.html',info=info, pg_name="Sign Up")
		flash("User has been created. Please advice them to log in on their device", 'info')
		return redirect(url_for('home'), 301)
	if request.method =="GET":
		return render_template('admin/Admin_add_new_user.html',info=info, pg_name="Add New User")






@site.route('/admin/add-new-item', methods=['POST','GET'])
def admin_add_new_item():
	ParseInfo()

	if request.method == "POST":
		form_data = request.form
		print (form_data)
		nItem = Admin_Add_Item(form_data['ItemNameForm'], form_data['ItemTypeForm'], form_data['ItemPriceForm'])
		nItem.add_item()

		return redirect(url_for('adminpage'))
	if request.method == "GET":
		return render_template('admin/admin_add_new_item.html', info=info, pg_name="Add New Item")

@site.route('/admin/delete-item', methods=['POST','GET'])
def admin_delete_item():
	ParseInfo()

	if request.method == "POST":
		form_data = request.form
		print (form_data)
		nItem = Admin_Add_Item(form_data['ItemNameForm'], form_data['ItemTypeForm'], form_data['ItemPriceForm'])
		nItem.add_item()

		return redirect(url_for('adminpage'))
	if request.method == "GET":
		dItem = Admin_Delete_Item("view")
		return render_template('admin/admin_delete_item.html', info=info, pg_name="Delete New Item", itemData = dItem.itemData)




@site.route('/admin/restart_server')
def restart_server():
	admin = admin_perm_check()
	if admin == True:
		shutdown_server()
		flash (f"Server Restart inititiated by {current_user.Username}", "warning")
	else:
		flash("Whoops! Looks like you don't have permission to do that! If you think this is a mistake, please contact support", "danger")
	return redirect(url_for('home'))




@site.route('/admin/purgekey')
def purgekey():
	admin = admin_perm_check()
	if admin == True:
		purge = sk()
		purge.purgeKey()
		return redirect(url_for('restart_server'))
	else:
		flash("Whoops! Looks like you don't have permission to do that! If you think this is a mistake, please contact support", "danger")
		return redirect(url_for('home'))

@site.route('/.well-known/acme-challenge/D5P4DM9Yke1xBVl_YFOM0ebVP1JCexDLnZ6DLf5k7j0')
def tempverify():
	return site.send_static_file('D5P4DM9Yke1xBVl_YFOM0ebVP1JCexDLnZ6DLf5k7j0')



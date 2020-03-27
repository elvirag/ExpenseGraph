import psycopg2
from flask import Flask

from expenses import Expense

app = Flask(__name__)
if app.config["ENV"] == "production":
	app.config.from_object("config.ProductionConfig")
else:
	app.config.from_object("config.DevelopmentConfig")

SELECT_EXPENSE_BASE_QUERY = """
		SELECT 
			exp_.Expense_Id,
			exp_.Date_purchase,
			exp_.Date_billing, 
			exp_.Name, 
			exp_.Cost, 
			cat."Name" as Category, 
			pt."Name" as Payment_Type, 
			bn."Name" as Business, 
			exp_.Comments 
		FROM 
			expenses exp_
			JOIN "Payment_Type" pt ON exp_.Payment_Type = pt.payment_type_id 
			JOIN categories cat ON cat."Category_id" = exp_.Category
			JOIN business bn ON bn."Business_id" = exp_.Business"""


def connect():
	conn = psycopg2.connect(
		user=app.config["DB_USERNAME"],
		password=app.config["DB_PASSWORD"],
		host=app.config["HOST_NAME"],
		port=app.config["DB_PORT"],
		dbname=app.config["DB_NAME"])
	cur = conn.cursor()

	return conn, cur


def create_expense(expense):
	conn, cur = connect()

	category_id = add_category(expense.category)
	payment_type_id = add_payment_type(expense.payment_type)
	pob_id = add_business(expense.business)

	create_expense_str = """INSERT INTO expenses (User_id, Date_purchase, Date_billing, Name, Cost, Category,
													Payment_Type, Business, Comments)
							VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
	expense_tuple = (
		expense.user_id, expense.date_purchase, expense.date_billed, expense.name, expense.cost, category_id,
		payment_type_id, pob_id, expense.comments)

	cur.execute(create_expense_str, expense_tuple)
	conn.commit()

	cur.execute("""SELECT max(Expense_id) FROM expenses WHERE expenses.User_id = 1""")
	conn.commit()

	expense_id = cur.fetchone()

	conn.close()

	return expense_id[0]


def get_expenses():
	conn, cur = connect()

	cur.execute(SELECT_EXPENSE_BASE_QUERY + "\n WHERE exp_.User_id = 1 ORDER BY exp_.Expense_Id ASC")

	expenses = cur.fetchall()

	conn.commit()
	conn.close()

	return expenses


def get_expense(expense_id):
	conn, cur = connect()

	exe_str = SELECT_EXPENSE_BASE_QUERY + \
			  "\nWHERE exp_.Expense_id={} AND exp_.User_id = 1\nORDER BY exp_.Expense_Id ASC".format(expense_id)
	cur.execute(exe_str)

	expense = cur.fetchone()

	conn.commit()
	conn.close()

	return expense


def delete_expense(expense_id):
	conn, cur = connect()

	delete_expense_str = """DELETE FROM expenses
							WHERE expenses.Expense_id=%s"""

	cur.execute(delete_expense_str, (expense_id,))

	conn.commit()
	conn.close()

	return cur.rowcount == 1


def update_expense(data):
	conn, cur = connect()

	expense = Expense(data)
	category_id = add_category(expense.category)
	payment_type_id = add_payment_type(expense.payment_type)
	pob_id = add_business(expense.business)

	create_expense_str = """UPDATE expenses
								SET Date_purchase=%s, Date_billing=%s, Name=%s,
								Cost=%s, Category=%s, Payment_Type=%s, Business=%s,
								Comments=%s
								WHERE expenses.Expense_Id=%s"""

	expense_tuple = (
		expense.date_purchase, expense.date_billed, expense.name, expense.cost, category_id, payment_type_id, pob_id,
		expense.comments, expense.expense_id)

	cur.execute(create_expense_str, expense_tuple)

	conn.commit()
	conn.close()

	return cur.rowcount == 1


def add_category(name, explanation="", user_id=1):
	conn, cur = connect()

	# TODO: change hard-coded
	select_category_id_str = """SELECT "Category_id" FROM categories WHERE "Name"=%s AND "User_id" = %s"""

	cur.execute(select_category_id_str, (name, user_id))
	conn.commit()

	category_id = cur.fetchone()
	if category_id:
		return category_id[0]

	cur.execute("""INSERT INTO categories ("User_id", "Name", "Explanation") VALUES(%s, %s, %s)""",
				(user_id, name, explanation))
	conn.commit()

	cur.execute(select_category_id_str, (name, user_id))
	category_id = cur.fetchone()
	conn.commit()

	conn.close()

	return category_id[0]


def get_categories():
	conn, cur = connect()

	cur.execute('SELECT * FROM categories')

	categories = cur.fetchall()

	conn.commit()
	conn.close()

	return categories


# TODO: Move payment type to scripts, let user choose from known types of payment
def add_payment_type(name):
	conn, cur = connect()

	select_payment_type_str: str = """SELECT payment_type_id FROM "Payment_Type" WHERE "Name"=%s"""

	cur.execute(select_payment_type_str, (name,))
	conn.commit()

	payment_type_id = cur.fetchone()
	if payment_type_id:
		return payment_type_id[0]

	cur.execute("""INSERT INTO "Payment_Type" ("Name") VALUES(%s)""", (name,))
	conn.commit()

	cur.execute(select_payment_type_str, (name,))
	conn.commit()

	payment_type_id = cur.fetchone()

	conn.close()

	return payment_type_id[0]


def get_payment_types():
	conn, cur = connect()

	cur.execute('SELECT * FROM "Payment_Type"')

	payment_types_tuple = cur.fetchall()
	payment_types = []

	conn.commit()
	conn.close()

	for payment_type_tuple in payment_types_tuple:
		payment_types.append(payment_type_tuple[1])

	return payment_types


def add_business(name):
	conn, cur = connect()

	select_business_id_sir = """SELECT "Business_id" FROM business WHERE "Name"=%s"""

	cur.execute(select_business_id_sir, (name,))
	conn.commit()

	business_id = cur.fetchone()
	if business_id:
		return business_id[0]

	cur.execute("""INSERT INTO business ("Name") VALUES( %s) RETURNING "Business_id" """, (name,))
	conn.commit()

	cur.execute(select_business_id_sir, (name,))
	conn.commit()
	business_id = cur.fetchone()

	conn.close()

	return business_id[0]


def get_businesses():
	conn, cur = connect()

	cur.execute('SELECT * FROM business')

	businesses_tuple = cur.fetchall()
	businesses = []

	conn.commit()
	conn.close()

	for business_tuple in businesses_tuple:
		businesses.append(business_tuple[1])

	return businesses

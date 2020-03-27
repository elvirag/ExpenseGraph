import psycopg2
from flask import Flask


def connect():
	conn = psycopg2.connect(
		user=app.config["DB_USERNAME"],
		password=app.config["DB_PASSWORD"],
		host=app.config["HOST_NAME"],
		port=app.config["DB_PORT"],
		dbname=app.config["DB_NAME"])
	cur = conn.cursor()

	return conn, cur


def create_users_table():
	conn, cur = connect()

	cur.execute("""
		CREATE TABLE IF NOT EXISTS users (
			User_id SERIAL PRIMARY KEY,
			User_name Varchar(256) NOT NULL,
			email citext not null unique,
			password_digest varchar not null,
			Subscription_active BOOL NOT NULL
		)
	""")

	conn.commit()
	conn.close()


app = Flask(__name__)
if app.config["ENV"] == "production":
	app.config.from_object("config.ProductionConfig")
else:
	app.config.from_object("config.DevelopmentConfig")


def init_db():
	create_categories_table()
	create_payment_type_table()
	create_business_table()
	create_expenses_table()


def create_expenses_table():
	conn, cur = connect()

	cur.execute("""
		CREATE TABLE IF NOT EXISTS expenses (
			Expense_id SERIAL PRIMARY KEY,
			User_id INTEGER NOT NULL,
			Date_purchase DATE NOT NULL,
			Date_billing DATE NOT NULL,
			Name Varchar(256) NOT NULL,
			Cost REAL NOT NULL,
			Category INTEGER NOT NULL,
			Payment_Type INTEGER NOT NULL,
			Business INTEGER NOT NULL,
			Comments Varchar(1024)
		)
	""")

	conn.commit()
	conn.close()


def create_categories_table():
	conn, cur = connect()

	cur.execute("""
		CREATE TABLE IF NOT EXISTS "categories" (
			"Category_id" SERIAL,
			"User_id" INTEGER NOT NULL,
			"Name" Varchar(256) NOT NULL UNIQUE,
			"Explanation" Varchar(512),
			PRIMARY KEY("Category_id")
		)
	""")

	conn.commit()
	conn.close()


def create_payment_type_table():
	conn, cur = connect()

	cur.execute("""
		CREATE TABLE IF NOT EXISTS "Payment_Type" (
			"payment_type_id" SERIAL,
			"Name"  Varchar(256) NOT NULL UNIQUE,
			PRIMARY KEY("payment_type_id")
		)
	""")

	conn.commit()
	conn.close()


def create_business_table():
	conn, cur = connect()

	cur.execute("""
		CREATE TABLE IF NOT EXISTS "business" (
			"Business_id" SERIAL,
			"Name"  Varchar(256) NOT NULL UNIQUE,
			PRIMARY KEY("Business_id")
		)
	""")

	conn.commit()
	conn.close()


def reset_db():
	conn, cur = connect()

	cur.execute("""
		DROP TABLE "Payment_Type";
		DROP TABLE expenses;
		DROP TABLE categories;
		DROP TABLE business;
	""")

	conn.commit()
	conn.close()


reset_db()
init_db()

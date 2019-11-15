import sqlite3

def connect():

	conn = sqlite3.connect('expenses_db.sqlite')
	cur = conn.cursor()

	return conn, cur

def create_expenses_table():
	conn, cur = connect()

	cur.execute('pragma encoding')

	cur.execute("""CREATE TABLE IF NOT EXISTS expenses (
	    Expense_id INTEGER PRIMARY KEY,
	    Date_purchase DATE NOT NULL,
	    Name Varchar(256) NOT NULL,
	    Cost REAL NOT NULL,
	    Category Varchar(256) NOT NULL,
	    Means Varchar(256) NOT NULL,
	    Buisness Varchar(256) NOT NULL,
	    Comments Varchar(1024)
	);
	""")

	conn.commit()
	conn.close()

def create_categories_table():
	conn, cur = connect()

	cur.execute('pragma encoding')

	cur.execute("""CREATE TABLE IF NOT EXISTS categories (
	    Category_id INTEGER PRIMARY KEY,
	    Name Varchar(256) NOT NULL UNIQUE,
	    Explanation Varchar(512)
	);
	""")

	conn.commit()

	cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='{0}';""".format("categories"))

	result = cur.fetchone()

	conn.close()

	return result

def prefill_categories_table():
	pass


def create_expense(date, name, cost, category, means, pob, comments=""):
	conn, cur = connect()

	cur.execute(
		"""INSERT INTO expenses (Date_purchase, Name, Cost, Category, Means, Buisness, Comments)
		VALUES( "{}", "{}", {}, "{}", "{}", "{}", "{}");
		""".format(date, name, cost, category, means, pob, comments)
	)

	conn.commit()
	conn.close()

def get_expenses():
	conn, cur = connect()

	cur.execute('SELECT * FROM expenses')

	expenses = cur.fetchall()

	conn.commit()
	conn.close()

	return expenses

def add_category(name, explanation=""):
	conn, cur = connect()

	cur.execute("""INSERT INTO categories (Name, Explanation)
		VALUES( "{}", "{}");""".format(name, explanation))

	conn.commit()
	conn.close()

def get_categories():
	conn, cur = connect()

	cur.execute('SELECT * FROM categories')

	categories = cur.fetchall()

	conn.commit()
	conn.close()

	return categories

def init_db():
	create_expenses_table()
	if create_categories_table():
		prefill_categories_table()
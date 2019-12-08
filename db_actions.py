import sqlite3

SELECT_EXPENSE_BASE_QUERY = """
        SELECT 
          expenses.Expense_Id,
          expenses.Date_purchase, 
          expenses.Name, 
          expenses.Cost, 
          categories.Name as Category, 
          Payment_Type.Name as Payment_Type, 
          business.Name as Business, 
          expenses.Comments 
        FROM 
          expenses 
          JOIN Payment_Type ON expenses.Payment_Type = Payment_Type.payment_type_id 
          JOIN categories ON categories.Category_id = expenses.Category 
          JOIN business ON business.Business_id = expenses.Business"""


def connect():
    conn = sqlite3.connect('expenses_db.sqlite')
    cur = conn.cursor()

    return conn, cur


def create_expenses_table():
    conn, cur = connect()

    cur.execute('pragma encoding')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            Expense_id INTEGER PRIMARY KEY,
            Date_purchase DATE NOT NULL,
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

    cur.execute('pragma encoding')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "categories" (
            "Category_id" INTEGER,
            "Name" Varchar(256) NOT NULL UNIQUE,
            "Explanation" Varchar(512),
            PRIMARY KEY("Category_id")
        )
    """)

    conn.commit()

    conn.close()


def create_expense(date, name, cost, category, payment_type, pob, comments=""):
    conn, cur = connect()

    category_id = add_category(category)
    payment_type_id = add_payment_type(payment_type)
    pob_id = add_business(pob)

    create_expense_str = """INSERT INTO expenses (Date_purchase, Name, Cost, Category, Payment_Type, Business, Comments)
                            VALUES(?, ?, ?, ?, ?, ?, ?)"""

    expense_tuple = (date, name, cost, category_id, payment_type_id, pob_id, comments)

    cur.execute(create_expense_str, expense_tuple)

    expense_id = cur.lastrowid

    conn.commit()
    conn.close()

    return expense_id


def get_expenses():
    conn, cur = connect()

    cur.execute(SELECT_EXPENSE_BASE_QUERY)

    expenses = cur.fetchall()

    conn.commit()
    conn.close()

    return expenses


def add_category(name, explanation=""):
    conn, cur = connect()

    cur.execute("""SELECT Category_id FROM categories WHERE Name=?""", (name,))
    conn.commit()

    category_id = cur.fetchone()
    if category_id:
        return category_id[0]

    cur.execute("""INSERT INTO categories (Name, Explanation) VALUES(?, ?)""", (name, explanation))

    category_id = cur.lastrowid

    conn.commit()
    conn.close()

    return category_id


def get_categories():
    conn, cur = connect()

    cur.execute('SELECT * FROM categories')

    categories = cur.fetchall()

    conn.commit()
    conn.close()

    return categories


def create_payment_type_table():
    conn, cur = connect()

    cur.execute('pragma encoding')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Payment_Type" (
            "payment_type_id"   INTEGER,
            "Name"  Varchar(256) NOT NULL UNIQUE,
            PRIMARY KEY("payment_type_id")
        )
    """)

    conn.commit()

    conn.close()


def add_payment_type(name):
    conn, cur = connect()

    cur.execute("""SELECT payment_type_id FROM Payment_Type WHERE Name=?""", (name,))
    conn.commit()

    payment_type_id = cur.fetchone()
    if payment_type_id:
        return payment_type_id[0]

    cur.execute("""INSERT INTO Payment_Type (Name) VALUES(?)""", (name,))

    payment_type_id = cur.lastrowid

    conn.commit()
    conn.close()

    return payment_type_id


def get_payment_types():
    conn, cur = connect()

    cur.execute('SELECT * FROM Payment_Type')

    payment_types_tuple = cur.fetchall()
    payment_types = []

    conn.commit()
    conn.close()

    for payment_type_tuple in payment_types_tuple:
        payment_types.append(payment_type_tuple[1])

    return payment_types


def create_business_table():
    conn, cur = connect()

    cur.execute('pragma encoding')

    cur.execute("""
        CREATE TABLE IF NOT EXISTS "business" (
            "Business_id" INTEGER,
            "Name"  Varchar(256) NOT NULL UNIQUE,
            PRIMARY KEY("Business_id")
        )
    """)

    conn.commit()

    conn.close()


def add_business(name):
    conn, cur = connect()

    cur.execute("""SELECT Business_id FROM business WHERE Name=?""", (name,))
    conn.commit()

    business_id = cur.fetchone()
    if business_id:
        return business_id[0]

    cur.execute("""INSERT INTO business (Name) VALUES( ?)""", (name,))

    business_id = cur.lastrowid

    conn.commit()
    conn.close()

    return business_id


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


def init_db():
    create_expenses_table()
    create_categories_table()
    create_payment_type_table()
    create_business_table()


def delete_expense():
    return None


# Make a patch type update - later
def update_expense(data):
    conn, cur = connect()

    expense = dict(data)
    category_id = add_category(expense.get("category"))
    payment_type_id = add_payment_type(expense.get("payment_type"))
    pob_id = add_business(expense.get("pob"))

    create_expense_str = """UPDATE expenses
                                SET Date_purchase=?, Name=?, Cost=?, Category=?, Payment_Type=?, Business=?, Comments=?
                                WHERE expenses.Expense_Id=?"""

    expense_tuple = (
        expense.get("date"), expense.get("name"), expense.get("cost"), category_id, payment_type_id, pob_id,
        expense.get("comments"), expense.get("expense_id"))

    result = cur.execute(create_expense_str, expense_tuple)

    conn.commit()
    conn.close()

    return result.rowcount == 1


def get_expense(expense_id):
    conn, cur = connect()

    exe_str = SELECT_EXPENSE_BASE_QUERY + "\nWHERE expenses.Expense_Id={}".format(expense_id)
    cur.execute(exe_str)

    expense = cur.fetchone()

    conn.commit()
    conn.close()

    return expense

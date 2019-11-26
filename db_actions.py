import sqlite3

EXPENSE_STRING = """
        SELECT 
          expenses.Expense_Id,
          expenses.Date_purchase, 
          expenses.Name, 
          expenses.Cost, 
          categories.Name as Category, 
          means.Name as Means, 
          business.Name as Business, 
          expenses.Comments 
        FROM 
          expenses 
          JOIN means ON expenses.means = means.Means_id 
          JOIN categories ON categories.Category_id = expenses.Category 
          JOIN business ON business.Business_id = expenses.Business;
    """


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
        Category INTEGER NOT NULL,
        Means INTEGER NOT NULL,
        Business INTEGER NOT NULL,
        Comments Varchar(1024)
    );
    """)

    conn.commit()
    conn.close()


def create_categories_table():
    conn, cur = connect()

    cur.execute('pragma encoding')

    cur.execute("""CREATE TABLE IF NOT EXISTS "categories" (
    "Category_id"   INTEGER,
    "Name"  Varchar(256) NOT NULL UNIQUE,
    "Explanation"   Varchar(512),
    PRIMARY KEY("Category_id")
    );""")

    conn.commit()

    conn.close()


def create_expense(date, name, cost, category, means, pob, comments=""):
    conn, cur = connect()

    category_id = add_category(category)
    means_id = add_means(means)
    pob_id = add_business(pob)

    create_expense_str = """INSERT INTO expenses (Date_purchase, Name, Cost, Category, Means, Business, Comments)
                            VALUES(?, ?, ?, ?, ?, ?, ?);"""

    expense_tuple = (date, name, cost, category_id, means_id, pob_id, comments)

    cur.execute(create_expense_str, expense_tuple)

    expense_id = cur.lastrowid

    conn.commit()
    conn.close()

    return expense_id


def get_expenses():
    conn, cur = connect()

    cur.execute(EXPENSE_STRING)

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

    cur.execute("""INSERT INTO categories (Name, Explanation)
                    VALUES( ?, ?);""", (name, explanation))

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


def create_means_table():
    conn, cur = connect()

    cur.execute('pragma encoding')

    cur.execute("""CREATE TABLE IF NOT EXISTS "means" (
    "Means_id"   INTEGER,
    "Name"  Varchar(256) NOT NULL UNIQUE,
    PRIMARY KEY("Means_id")
    );""")

    conn.commit()

    conn.close()


def add_means(name):
    conn, cur = connect()

    cur.execute("""SELECT Means_id FROM means WHERE Name=?""", (name,))
    conn.commit()

    means_id = cur.fetchone()
    if means_id:
        return means_id[0]

    cur.execute("""INSERT INTO means (Name)
                    VALUES( ?);""", (name,))

    means_id = cur.lastrowid

    conn.commit()
    conn.close()

    return means_id


def get_means():
    conn, cur = connect()

    cur.execute('SELECT * FROM means')

    means_tuple = cur.fetchall()
    means = []

    conn.commit()
    conn.close()

    for mean_tuple in means_tuple:
        means.append(mean_tuple[1])

    return means


def create_business_table():
    conn, cur = connect()

    cur.execute('pragma encoding')

    cur.execute("""CREATE TABLE IF NOT EXISTS "business" (
    "Business_id"   INTEGER,
    "Name"  Varchar(256) NOT NULL UNIQUE,
    PRIMARY KEY("Business_id")
    );""")

    conn.commit()

    conn.close()


def add_business(name):
    conn, cur = connect()

    cur.execute("""SELECT Business_id FROM business WHERE Name=?""", (name,))
    conn.commit()

    business_id = cur.fetchone()
    if business_id:
        return business_id[0]

    cur.execute("""INSERT INTO business (Name)
                    VALUES( ?);""", (name,))

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
    create_means_table()
    create_business_table()


def delete_expense():
    return None


# Make a patch type update - later
def update_expense(data):
    conn, cur = connect()

    expense = dict(data)
    category_id = add_category(expense.get("category"))
    means_id = add_means(expense.get("means"))
    pob_id = add_business(expense.get("pob"))

    create_expense_str = """UPDATE expenses
                                SET Date_purchase=?, Name=?, Cost=?, Category=?, Means=?, Business=?, Comments=?
                                WHERE expenses.Expense_Id=?;"""

    expense_tuple = (
        expense.get("date"), expense.get("name"), expense.get("cost"), category_id, means_id, pob_id,
        expense.get("comments"), expense.get("expense_id"))

    result = cur.execute(create_expense_str, expense_tuple)

    conn.commit()
    conn.close()

    return result.rowcount == 1


def get_expense(expense_id):
    conn, cur = connect()

    exe_str = EXPENSE_STRING[:-6] + "\nWHERE expenses.Expense_Id={};".format(expense_id)
    cur.execute(exe_str)

    expense = cur.fetchone()

    conn.commit()
    conn.close()

    return expense

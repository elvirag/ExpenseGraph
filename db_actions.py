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
        Business Varchar(256) NOT NULL,
        Comments Varchar(1024)
    );
    """)

    conn.commit()
    conn.close()


def create_categories_table():
    conn, cur = connect()

    cur.execute('pragma encoding')

    cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='{0}';""".format("categories"))

    result = cur.fetchone()

    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS "categories" (
    "Category_id"   INTEGER,
    "Name"  Varchar(256) NOT NULL UNIQUE,
    "Explanation"   Varchar(512),
    PRIMARY KEY("Category_id")
    );""")

    conn.commit()

    if result is None:
        cur.execute("""INSERT INTO "categories" VALUES
                                    (1,'Salary',''),
                                    (2,'Rent',''),
                                    (3,'Pets',''),
                                    (4,'Bills',''),
                                    (5,'Groceries',''),
                                    (6,'Cleaning Supplies',''),
                                    (7,'Restaurants','');
                    """)
        conn.commit()

    conn.close()


def create_expense(date, name, cost, category, means, pob, comments=""):
    conn, cur = connect()

    create_expense_str = """INSERT INTO expenses
        VALUES( %(date)s, %(name)s, %(name)s, %(category)s, %(means)s, %(pob)s);
        """
    expense_dict = {
        'date': date, 'name': name, 'cost': cost, 'category': category, 'means': means, 'pob': pob,
    }
    if comments:
        create_expense_str = create_expense_str[-2] + ", %(comments)s);"
        expense_dict['comments'] = comments

    ans = create_expense_str % expense_dict
    print(ans)
    cur.execute(ans)

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
    create_categories_table()

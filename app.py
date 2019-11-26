from flask import Flask, request, render_template, redirect, url_for
from flask_babel import Babel, gettext
from werkzeug.utils import secure_filename

import db_actions
import excel_actions

app = Flask(__name__)
babel = Babel(app)


@app.route('/')
def main():
    db_actions.init_db()
    expenses = db_actions.get_expenses()
    return render_template('index.html', expenses=expenses)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/excel')
def excel():
    rows = excel_actions.return_sheet()

    return render_template('excel.html', rows=rows)


@app.route('/excel_import', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))

        excel_actions.import_excel(f.filename)
        return redirect(url_for('main'))


@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'GET':
        categories = db_actions.get_categories()
        means_types = db_actions.get_means()
        businesses = db_actions.get_businesses()

        return render_template('add_expense.html', categories=categories, means_types=means_types,
                               businesses=businesses)

    elif request.method == 'POST':
        date = request.form.get('date')
        name = request.form.get('name')
        cost = request.form.get('cost')
        category = request.form.get('category')
        means = request.form.get('means')
        business = request.form.get('business')
        comments = request.form.get('comments')

        if db_actions.create_expense(date, name, cost, category, means, business, comments):
            expenses = db_actions.get_expenses()
            return render_template('index.html', expenses=expenses)
        else:
            return gettext("Your expense wasn't created :(")


# TODO: need to do partial update, ans also add a message if expense is the same, via html.
@app.route('/update_expense', methods=['POST'])
def update_expense():
    if request.method == 'POST':
        if 'updated_expense' in request.form:
            success = db_actions.update_expense(request.form)
            if success:
                return redirect(url_for('main'))
            else:
                return gettext("Your expense wasn't updated :(")
        else:
            expense_id = request.form['expense_to_update']
            expense = db_actions.get_expense(expense_id)
            categories = db_actions.get_categories()
            means_types = db_actions.get_means()
            businesses = db_actions.get_businesses()

            return render_template('update_expense.html', expense=expense, categories=categories,
                                   means_types=means_types, businesses=businesses)


# TODO: Need to delete also businesses, means and categories - just check if something uses them, and if not, remove
@app.route('/delete_expense', methods=['DELETE'])
def delete_expense():
    if request.method == 'DELETE':
        db_actions.delete_expense()

        return redirect(url_for('main'))


@app.route('/add_category', methods=['POST'])
def add_category():
    category_name = request.form.get('category')
    category_explanation = request.form.get('explanation')

    db_actions.add_category(category_name, category_explanation)
    expenses = db_actions.get_expenses()
    # TODO: Add returning to previously filled form, with saving state of form before going to add expenses
    return render_template('index.html', expenses=expenses)


@app.route('/edit_category')
def edit_category():
    pass


@app.route('/delete_category')
def delete_category():
    pass


if __name__ == "__main__":
    app.run(debug=True)

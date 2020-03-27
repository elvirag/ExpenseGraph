from flask import Flask, request, render_template, redirect, url_for
from flask_babel import gettext
from werkzeug.utils import secure_filename

import db_actions
import excel_actions
import expenses

app = Flask(__name__)


@app.route('/')
def main():
	expenses_data = expenses.get_expenses()
	return render_template('index.html', expenses=expenses_data)


@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/excel')
def excel():
	rows = excel_actions.return_sheet()

	return render_template('excel.html', rows=rows)


@app.route('/excel_import', methods=['POST'])
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
		payment_types = db_actions.get_payment_types()
		businesses = db_actions.get_businesses()

		return render_template('add_expense.html', categories=categories, payment_types=payment_types,
							   businesses=businesses)

	elif request.method == 'POST':
		if expenses.create_expense(request.form):
			expenses_data = expenses.get_expenses()
			return render_template('index.html', expenses=expenses_data)
		else:
			return gettext("Your expense wasn't created :(")


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
			expense = expenses.get_expense(expense_id)
			categories = db_actions.get_categories()
			payment_types = db_actions.get_payment_types()
			businesses = db_actions.get_businesses()

			return render_template('update_expense.html', expense=expense, categories=categories,
								   payment_types=payment_types, businesses=businesses)


@app.route('/delete_expense', methods=['POST'])
def delete_expense():
	expense_id = request.form['expense_to_delete']
	success = db_actions.delete_expense(expense_id)

	if success:
		return redirect(url_for('main'))
	else:
		return gettext("Your expense (id:" + expense_id + ") wasn't deleted :(")


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


# TODO: add delete category, display only non active categories


if __name__ == "__main__":
	app.run()

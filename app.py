from flask import Flask, request, render_template
from flask_babel import Babel, gettext
from werkzeug.utils import secure_filename

import db_actions
import excel_actions

app = Flask(__name__)
babel = Babel(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())


@app.route('/')
def main():
    db_actions.init_db()
    expenses = db_actions.get_expenses()
    return render_template('index.html', expenses=expenses)


@app.route('/excel')
def excel():
    rows = excel_actions.return_sheet()

    return render_template('excel.html', rows=rows)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))

        rows = excel_actions.return_sheet(f.filename)
        return render_template('excel.html', rows=rows)


@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'GET':
        categories = db_actions.get_categories()
        means_types = [
            gettext("Credit Card"),
            gettext("Cash"),
            gettext("Cheque"),
            gettext("Bank Deposit"),
            gettext("Salary")
        ]

        return render_template('add_expense.html', categories=categories, means_types=means_types)

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


@app.route('/edit_expense')
def edit_expense():
    pass


@app.route('/delete_expense')
def delete_expense():
    pass


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

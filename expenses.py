import db_actions

expense_keys = ["expense_id", "date_purchase", "name", "cost", "category", "payment_type", "business", "comments"]


def tuple_to_dict(expense):
    return dict(zip(expense_keys, expense))


def get_expenses():
    return [tuple_to_dict(x) for x in db_actions.get_expenses()]


def create_expense(form):
    expense_data = [form.get(key) for key in expense_keys[1:]]

    return db_actions.create_expense(*expense_data)

from dataclasses import dataclass
from datetime import date

import db_actions

expense_keys = ["expense_id", "date_purchase", "date_billed", "name", "cost", "category", "payment_type", "business",
				"comments"]


@dataclass
class Expense:
	"""Class for keeping track of expenses."""
	expense_id: int
	user_id: int
	date_purchase: date
	date_billed: date
	name: str
	cost: float
	category: str
	payment_type: str
	business: str
	comments: str = ""

	def __init__(self, expense_dict):
		self.expense_id = expense_dict['expense_id']
		self.date_purchase = expense_dict['date_purchase']
		if expense_dict['date_billed']:
			self.date_billed = expense_dict['date_billed']
		else:
			self.date_billed = expense_dict['date_purchase']
		self.name = expense_dict['name']
		self.cost = expense_dict['cost']
		self.category = expense_dict['category']
		self.payment_type = expense_dict['payment_type']
		self.business = expense_dict['business']
		self.comments = expense_dict['comments']
		self.user_id = 1  # expense_dict['user_id']  # TODO: change user_id to not hard coded


def tuple_to_dict(expense):
	return dict(zip(expense_keys, expense))


def get_expenses():
	return [Expense(tuple_to_dict(item)) for item in db_actions.get_expenses()]


def create_expense(form):
	expense_dict = {item: form.get(item) for item in expense_keys}
	expense = Expense(expense_dict)

	return db_actions.create_expense(expense)


def get_expense(expense_id):
	expense = db_actions.get_expense(expense_id)
	return Expense(tuple_to_dict(expense))

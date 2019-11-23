from datetime import datetime, timedelta

import xlrd

import db_actions


def return_sheet(filename="Expenses.xlsx"):
    # To open Workbook
    wb = xlrd.open_workbook(filename, encoding_override="utf-8")
    sheet = wb.sheet_by_name("פירוט הוצאות מדוקדק (אפליקציה)")

    rows = []

    for i in range(1, sheet.nrows):
        row = []
        date_value = sheet.cell(i, 0).value
        if date_value == '':
            break
        row.append((datetime(1899, 12, 31) + timedelta(days=int(date_value) - 1)).replace(microsecond=0).date())
        for j in range(1, 6):
            row.append(sheet.cell(i, j).value)
        rows.append(row)

    return rows


def export_excel(filename):
    pass


def update_categories_table(categories):
    for category in categories:
        db_actions.add_category(category)


def update_means_table(means):
    for mean in means:
        db_actions.add_means(mean)


def import_excel(filename):
    rows = return_sheet(filename)

    for row in rows:
        db_actions.create_expense(*row, '')

    return str(len(rows)) + "rows were imported successfully"

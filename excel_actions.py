from datetime import datetime, timedelta

import xlrd


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

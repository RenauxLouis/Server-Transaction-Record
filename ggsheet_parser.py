import gspread
import pandas as pd

FORMULA_COLUMNS = ["Type", "Laverie", "Réduction Type 1", "Réduction Type 2",
                   "Type de Réduction", "Prix à payer", "Prix Payé",
                   "Avoir",     "Code cb"]
MAP_COLUMN_TO_GGSHEET_COLUMN = {
    "Code": "A",
    "Type": "B",
    "Laverie": "C",
    "Machine": "D",
    "Jour": "E",
    "Heure": "F",
    "Date": "G",
    "Time": "H",
    "Réduction Type 1": "I",
    "Réduction Type 2": "J",
    "Type de Réduction": "K",
    "Prix à payer": "L",
    "Prix Payé": "M",
    "Avoir": "N",
    "Code cb": "O"
}


def connect_to_worksheet():
    gc = gspread.service_account()
    sheet = gc.open("LaveyLivrey").sheet1
    return sheet


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return len(str_list) + 1


def get_ggsheet_as_df():

    sheet = connect_to_worksheet()

    new_row_i = next_available_row(sheet)
    formulas = get_formulas_empty_cells(sheet, new_row_i)

    return formulas, new_row_i

def get_formulas_empty_cells(sheet, new_row_i):

    formulas = {}
    for formula_column in FORMULA_COLUMNS:
        column = MAP_COLUMN_TO_GGSHEET_COLUMN[formula_column]
        cell = column + str(new_row_i)
        formula = sheet.acell(cell, value_render_option="FORMULA").value
        formulas[column] = formula

    return formulas


def append_row_ggsheet(formulas, new_row_i, qrcode_input):

    qrcode_input = {
        MAP_COLUMN_TO_GGSHEET_COLUMN[k]: v for k, v in qrcode_input.items()}
    new_row = {**qrcode_input, **formulas}
    columns = sorted(list(MAP_COLUMN_TO_GGSHEET_COLUMN.values()))
    new_row_ordered = [new_row[column] for column in columns]

    sheet = connect_to_worksheet()
    sheet.insert_row(new_row_ordered, index=new_row_i,
                     value_input_option="USER_ENTERED")


if __name__ == "__main__":
    get_ggsheet_as_df()

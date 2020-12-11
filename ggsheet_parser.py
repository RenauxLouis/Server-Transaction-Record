import gspread

MAP_COLUMN_TO_GGSHEET_COLUMN = {
    "Code": "A",
    "Machine": "D",
    "Jour": "E",
    "Heure": "F",
    "Date": "G",
    "Time": "H"
}


def connect_to_worksheet():
    gc = gspread.service_account()
    sheet = gc.open("LaveyLivrey").sheet1
    return sheet


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return len(str_list) + 1


def append_row_ggsheet(qrcode_input):

    sheet = connect_to_worksheet()
    new_row_i = next_available_row(sheet)
    for column, value in qrcode_input.items():
        column = MAP_COLUMN_TO_GGSHEET_COLUMN[column]
        cell = column + str(new_row_i)

        sheet.update_acell(cell, value)

import gspread

GG_SHEET_NAME = "SBS Laverie Privée"
MAP_COLUMN_TO_GGSHEET_COLUMN = {
    "User": "A",
    "Code": "B",
    "Machine": "C",
    "Jour": "D",
    "Heure": "E",
    "Date": "F",
    "Time": "G"
}


def connect_to_sheet():
    gc = gspread.service_account()
    sheet = gc.open(GG_SHEET_NAME).sheet1
    return sheet


def next_available_row(sheet):
    str_list = list(filter(None, sheet.col_values(1)))
    return len(str_list) + 1


def append_row_ggsheet(qrcode_input, loads):

    sheet = connect_to_sheet()
    new_row_i = next_available_row(sheet)

    mapped_qrcode_input = {MAP_COLUMN_TO_GGSHEET_COLUMN[k]: v for k, v
                           in qrcode_input.items()}
    mapped_qrcode_input_sort = sorted(
        mapped_qrcode_input.items(), key=lambda item: item[0])
    cell_values = [pair[1] for pair in mapped_qrcode_input_sort]

    cells_to_update = []
    for load in range(loads):
        new_row_with_load = str(new_row_i + load)
        cell_list = sheet.range(f"A{new_row_with_load}:F{new_row_with_load}")
        for i, cell_value in enumerate(cell_values):
            cell_list[i].value = cell_value
        cells_to_update.extend(list(cell_list))

    sheet.update_cells(cells_to_update, value_input_option="USER_ENTERED")

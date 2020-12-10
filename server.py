from datetime import datetime

import pytz
from flask import Flask, Response, request, render_template
from waitress import serve

from ggsheet_parser import (FORMULA_COLUMNS, MAP_COLUMN_TO_GGSHEET_COLUMN,
                            connect_to_worksheet, get_ggsheet_as_df)

MAP_DAY_JOUR = {
    "Monday": "Lundi",
    "Tuesday": "Mardi",
    "Wednesday": "Mercredi",
    "Thursday": "Jeudi",
    "Friday": "Vendredi",
    "Saturday": "Samedi",
    "Sunday": "Dimanche",
}


app = Flask(__name__)


def get_time():

    tz = pytz.timezone('Europe/Paris')
    now = datetime.now(tz)
    jour = MAP_DAY_JOUR[now.strftime("%A")]
    time = now.strftime("%X")
    heure = time.split(":")[0]
    time_clean = time.split(".")[0]
    date = str(now.strftime("%d-%m-%Y"))

    return date, time_clean, jour, heure


@app.route("/is_alive", methods=["GET"])
def is_alive():
    return "Server is running"


@app.route("/add_transaction_row", methods=["GET"])
def add_transaction_row():

    code = request.args.get("code")
    machine = request.args.get("machine")

    date, time, jour, heure = get_time()

    qrcode_input = {
        "Code": code,
        "Machine": machine,
        "Jour": jour,
        "Heure": heure,
        "Date": date,
        "Time": time
    }

    sheet, sheet_columns, formulas, new_row_i = get_ggsheet_as_df()

    sheet = connect_to_worksheet()
    for column in FORMULA_COLUMNS:
        column = MAP_COLUMN_TO_GGSHEET_COLUMN[column]
        cell = column + str(new_row_i)

        formula = formulas[column]

        sheet.update_acell(cell, formula)

    for column, value in qrcode_input.items():
        column = MAP_COLUMN_TO_GGSHEET_COLUMN[column]
        cell = column + str(new_row_i)

        sheet.update_acell(cell, value)

    return render_template('success.html', error=error)

if __name__ == "__main__":
    serve(app, port=8080)

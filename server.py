from datetime import datetime

import pytz
from flask import Flask, Response, request
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

def get_jour_heure():

    tz = pytz.timezone('Europe/Paris')
    now = datetime.now(tz)
    jour = MAP_DAY_JOUR[now.strftime("%A")]
    time = now.strftime("%X")
    heure = time.split(":")[0]

    return jour, heure


app = Flask(__name__)


@app.route("/is_alive", methods=["GET"])
def is_alive():
    return "Server is running"


@app.route("/add_transaction_row", methods=["GET"])
def add_transaction_row():

    code = request.args.get("code")
    machine = request.args.get("machine")

    jour, heure = get_jour_heure()

    qrcode_input = {
        "Code": code,
        "Machine": machine,
        "Jour": jour,
        "Heure": heure
    }

    sheet, sheet_columns, formulas, new_row_i = get_ggsheet_as_df()


    sheet = connect_to_worksheet()
    for column in FORMULA_COLUMNS:
        column = MAP_COLUMN_TO_GGSHEET_COLUMN[column]
        cell = column + str(new_row_i)
        print(cell)

        formula = formulas[column]
        print(formula)

        sheet.update_acell(cell, formula)

    for column, value in qrcode_input.items():
        column = MAP_COLUMN_TO_GGSHEET_COLUMN[column]
        cell = column + str(new_row_i)
        print(cell)
        print(value)

        sheet.update_acell(cell, value)

    return Response("", status=200, mimetype="application/json")

if __name__ == "__main__":
    serve(app, port=8080)
from datetime import datetime
import os
from string import Template
import json
import logging

import pytz
from flask import Flask, request
from waitress import serve

from ggsheet_parser import append_row_ggsheet

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
app.secret_key = "dsfghytresdfgtr"

log_fname = "qr_code.log"
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()
logger.addHandler(logging.FileHandler(log_fname))


def get_time():

    tz = pytz.timezone('Europe/Paris')
    now = datetime.now(tz)
    logger.info(now)
    jour = MAP_DAY_JOUR[now.strftime("%A")]
    time = now.strftime("%X")
    heure = time.split(":")[0]
    time_clean = time.split(".")[0]
    date = str(now.strftime("%d-%m-%Y"))

    return date, time_clean, jour, heure


@app.route("/is_alive", methods=["GET"])
def is_alive():
    return "Server is running"


@app.route("/add_transaction_row_with_load", methods=["GET"])
def add_transaction_row():

    code = request.args.get("code")
    machine = request.args.get("machine")
    loads = int(request.args.get("loads"))

    print(code, machine, loads)

    date, time, jour, heure = get_time()

    qrcode_input = {
        "Code": code,
        "Machine": machine,
        "Jour": jour,
        "Heure": heure,
        "Date": date,
        "Time": time
    }
    logger.info(qrcode_input)
    logger.info(loads)

    append_row_ggsheet(qrcode_input, loads)

    return (json.dumps({"success": True}), 200,
            {"ContentType": "application/json"})


if __name__ == "__main__":
    serve(app, port=8080, threads=1)

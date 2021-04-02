from datetime import datetime
import os
from string import Template

import pytz
from flask import Flask, Response, request, session, redirect, url_for
from waitress import serve

from ggsheet_parser import append_row_ggsheet

HTML_FNAME = "success.html"
LOGIN_FNAME = "login.html"
MAP_DAY_JOUR = {
    "Monday": "Lundi",
    "Tuesday": "Mardi",
    "Wednesday": "Mercredi",
    "Thursday": "Jeudi",
    "Friday": "Vendredi",
    "Saturday": "Samedi",
    "Sunday": "Dimanche",
}

CODE = None
MACHINE = None

app = Flask(__name__)


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User: {self.username}>"


VALID_USERS = [
    User(id=1, username="samuel", password="jadorelescarottes")
]

def get_time():

    tz = pytz.timezone('Europe/Paris')
    now = datetime.now(tz)
    jour = MAP_DAY_JOUR[now.strftime("%A")]
    time = now.strftime("%X")
    heure = time.split(":")[0]
    time_clean = time.split(".")[0]
    date = str(now.strftime("%d-%m-%Y"))

    return date, time_clean, jour, heure


def write_html(code, machine):

    html_fpath = os.path.join("templates", HTML_FNAME)
    with open(html_fpath) as fi:
        html = fi.read()

    formatted_html = Template(html).safe_substitute(code=code, machine=machine)

    return formatted_html


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.pop("user_id", None)
        username = request.form["username"]
        password = request.form["password"]

        matching_user = [x for x in users if x.username == username][0]
        if matching_user and user.password == password:
            session["user_id"] = user.id
            formatted_html = write_html(code, machine)
            return formatted_html
        else:
            return redirect(url_for("login"))

    return "Server is running"


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

    append_row_ggsheet(qrcode_input)

    html_fpath = os.path.join("templates", LOGIN_FNAME)
    with open(html_fpath) as fi:
        html = fi.read()

    CODE = code
    MACHINE = machine

    return html


if __name__ == "__main__":
    serve(app, port=8080, threads=1)

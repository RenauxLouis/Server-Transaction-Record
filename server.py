from datetime import datetime
import os
from string import Template
from argparse import ArgumentParser

import pytz
from flask import (Flask, Response, request, session, make_response,
                   redirect, url_for, g, render_template)
from waitress import serve

from ggsheet_parser import append_row_ggsheet

SUCCESS_PAGE_FNAME = "success.html"
LOGIN_PAGE_FNAME = "new_login.html"
CONNECTED_PAGE_FNAME = "connected.html"
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

login_html_fpath = os.path.join("templates", LOGIN_PAGE_FNAME)
with open(login_html_fpath) as fi:
    LOGIN_HTML = fi.read()
login_html_fpath = os.path.join("templates", CONNECTED_PAGE_FNAME)
with open(login_html_fpath) as fi:
    CONNECTED_HTML = fi.read()
html_fpath = os.path.join("templates", SUCCESS_PAGE_FNAME)
with open(html_fpath) as fi:
    SUCCESS_HTML = fi.read()


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<User: {self.username}>"


parser = ArgumentParser()
parser.add_argument("--username", type=str)
parser.add_argument("--password", type=str)
args = parser.parse_args()

VALID_USERS = [
    User(id=1, username=args.username, password=args.password)
]
VALID_USERNAMES = [user.username for user in VALID_USERS]


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

    formatted_html = Template(SUCCESS_HTML).safe_substitute(
        code=code, machine=machine)

    return formatted_html


def write_html_login(error_message=""):

    formatted_html = Template(LOGIN_PAGE_FNAME).safe_substitute(
        error_message=error_message)

    return formatted_html


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        session.pop("user_id", None)
        username = request.form["username"]
        password = request.form["password"]

        matching_users = [x for x in VALID_USERS if x.username == username]
        if not matching_users:

            error_message = "Identifiant ou Mot de Passe incorrect.\nVeuillez"\
                            "confirmer avec Samuel Gérard pour confirmation"
            return render_template(write_html_login(error_message))
        else:
            matching_user = matching_users[0]
            if matching_user.password == password:
                session["user_id"] = matching_user.id

                resp = make_response(SUCCESS_HTML)
                resp.set_cookie("user", matching_user.username)
                return resp

    return render_template(write_html_login())


@app.route("/is_alive", methods=["GET"])
def is_alive():
    return "Server is running"


@app.route("/add_transaction_row", methods=["GET"])
def add_transaction_row():

    user = request.cookies.get("user")
    print(user)
    if not user in VALID_USERNAMES:
        return redirect("https://qrcodelaveylivrey.com/login")

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

    formatted_html = write_html(code, machine)

    return formatted_html

@app.before_request
def before_request():
    g.user = None

    if "user_id" in session:
        user = [x for x in VALID_USERS if x.id == session["user_id"]][0]
        g.user = user


@app.route("/profile")
def profile():
    if not g.user:
        return redirect(url_for("login"))

    return render_template("profile.html")


if __name__ == "__main__":
    serve(app, port=8080, threads=1)

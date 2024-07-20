import sqlite3

from flask import Flask, render_template, request, redirect
from markupsafe import escape

from src.components.user import User
from src.components.database import Database

app = Flask(__name__)


def withdraw_money(_id: int, money: int):
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()

    # data = cursor.execute(f"select balance from atm where id={_id}")

    cursor.execute(f"update atm set balance=balance-{money} where id={_id}")

    conn.commit()
    conn.close()


# def withdraw_money(_id: int, money: int):
#     conn = sqlite3.connect("atm.db")
#     cursor = conn.cursor()

#     cursor.execute(f"update atm set balance=balance-{money} where id={_id}")

#     conn.commit()
#     conn.close()


def check_balance(_id: int):
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()

    data = cursor.execute(f"select * from atm where id={_id}")
    res = [row for row in data]

    if len(res) > 0:
        _id, fname, lname, acc_no, password, acc_type, balance = [row for row in data]

    conn.commit()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/atm", methods=["GET", "POST"])
def atm():
    if request.method == "POST":
        acc_no = request.form["acc_no"]
        password = request.form["password"]
        amount = request.form["amount"]

        user = User()

        _id = user.search_user(acc_no, password)

        withdraw_money(_id, amount)

        return render_template("atm.html")

    if request.method == "GET":
        account = request.form.get("account", False)
        password = request.form.get("password", False)

        user = User()

        _id = user.search_user(account, password)

        check_balance(_id)

        return render_template("atm.html")

    return render_template("atm.html")


@app.route("/create_user", methods=["GET", "POST"])
def singup():
    if request.method == "POST":
        fname = request.form, ["fname"]
        lname = request.form["lname"]
        acc_type = request.form["acc_type"]
        password = request.form["password"]

        print([fname, lname, acc_type, password])

        data = (fname, lname, acc_type, password)

        user = User()
        res = user.create_user(data)

        if res:
            return redirect("/atm")

        else:
            return "Something went wrong!"

    return render_template("create_user.html")


@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

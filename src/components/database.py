import sqlite3
from typing import Tuple

# from cryptography.fernet import Fernet
import numpy as np


class Database:
    def __init__(self) -> None:
        pass

    def create_table(self):
        conn = sqlite3.connect("atm.db")

        cursor = conn.cursor()
        table = """
                create table if not exists atm(
                    id integer primary key autoincrement,
                    fname varchar(30),
                    lname varchar(30),
                    acc_no integer unique,
                    password varchar(30),
                    acc_type varchar(30),
                    balance integer default 0
                )
                """
        cursor.execute(table)
        conn.close()

    def check_acc_exists(self, acc_no: int):
        conn = sqlite3.connect("atm.db")
        cursor = conn.cursor()

        data = cursor.execute(
            f"SELECT exists(SELECT 1 FROM atm WHERE acc_no={acc_no}) AS row_exists;"
        )
        check_acc_exists = [row[0] for row in data][0]

        if check_acc_exists > 0:
            acc_no = np.random.randint(100000, 999999)
            check_acc_exists(acc_no)

        conn.close()

    def insert(self, data: Tuple):
        conn = sqlite3.connect("atm.db")
        cursor = conn.cursor()

        fname, lname, acc_type, password = data

        acc_no = np.random.randint(100000, 999999)

        data = cursor.execute(
            f"SELECT exists(SELECT 1 FROM atm WHERE acc_no={acc_no}) AS row_exists;"
        )

        self.check_acc_exists(acc_no)

        print(data)

        query = f"insert into atm(fname, lname, acc_type, password, acc_no) values('{fname}', '{lname}', '{acc_type}', {password}, {acc_no})"
        cursor.execute(query)

        print(acc_no)

        conn.commit()
        conn.close()

    def search_id(self, acc_no: int, password: int):
        conn = sqlite3.connect("atm.db")
        cursor = conn.cursor()

        data = cursor.execute(
            f"SELECT id FROM atm WHERE acc_no={acc_no} AND password={password};"
        )
        # check_acc_exists = [row[0] for row in data][0]
        result = [row[0] for row in data]
        if len(result) > 0:
            return result[0]

        conn.close()

        return False

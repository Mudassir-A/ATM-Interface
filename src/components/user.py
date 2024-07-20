from typing import Tuple

from cryptography.fernet import Fernet

from src.components.database import Database

key = Fernet.generate_key()
fernet = Fernet(key)


class User:
    def __init__(self) -> None:
        self.fname: str
        self.lname: str
        self.acc_type: str
        self.password: str
        self.balance: int

    def create_user(self, data: Tuple):
        try:
            fname, lname, acc_type, password = data

            self.fname = fname
            self.lname = lname
            self.acc_type = acc_type
            self.password = fernet.encrypt(password.encode())
            self.balance = 0

            db = Database()
            db.create_table()

            db.insert(data)

            return True

        except Exception as e:
            print(e)
        

    def search_user(self, acc_no: int, password: int):
        db = Database()
        _id = db.search_id(acc_no, password)

        return _id

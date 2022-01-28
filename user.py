import sys
import os
from dotenv import load_dotenv
import csv
import hashlib


load_dotenv(verbose=True)

KEY = os.getenv("KEY")
PASSWORD = hashlib.sha256((os.getenv("PASSWORD") + KEY).encode()).hexdigest()
FILE = "user.csv"


def checkPasswordValidation(pw: str):
    pw = pw + KEY
    encoded_pw = hashlib.sha256(pw.encode()).hexdigest()

    return encoded_pw == PASSWORD


def createUser(id: str):
    f = open(FILE, "a", newline="")
    writer = csv.writer(f)
    writer.writerow([id])
    return True


def confirmUser(id: str):
    with open(FILE) as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            if id == row[0]:
                return True

    return False

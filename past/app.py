"""
Medical appointments website
"""


from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

from project import *
from werkzeug.security import check_password_hash, generate_password_hash


# Initialize app
app = Flask(__name__)
app.secret_key = "very top secret key mr sirrrr"

# Session is 31 days by default (remind user to create an account)
app.config["SESSION_PERMANENT"] = True
# Store session data in server files
app.config["SESSION_TYPE"] = "filesystem"
# Initialize the session
Session(app)

# Databases
users = SQL("sqlite:///users.db")


def main():
    ...

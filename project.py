"""
Medical appointments system
"""
from helpers import *


def main():
    login_page()


def register_page():
    # User login information
    name, email, password, confirm = ""

    # Ask for user information
    border("Register your account")
    print("If already have an account, type '-login' instead!")

    # Input data while checking for the login command
    name = input("Name: ").strip()
    if name.lower() == "-login":
        login_page()

    email = input("Email: ").strip()
    if email.lower() == "-login":
        login_page()

    password = input("Password: ").strip()
    if password.lower() == "-login":
        login_page()

    confirm = input("Confirm assword: ").strip()
    if confirm.lower() == "-login":
        login_page()

    if not name or not email or not password:
        print("Missing required input")
        register_page()

    if name.isnumeric() or email.isnumeric():
        print("Invalid name and/or email")
        register_page()
    
    


def login_page():
    ...


def home_page():
    ...


def schedule_page():
    ...


def receipts_page():
    ...


def reports_page():
    ...


def receipt_page():
    ...


def report_page():
    ...


if __name__ == "__main__":
    main()

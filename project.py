"""
Medical appointments system
"""
from helpers import *


def main():
    clear_terminal()
    register_page()


def register_page():
    for _ in range(5):
        # [name, email, password, confirm]
        info = []

        # Ask for user information
        page = "Register your account\n"
        page += "If you already have an account or you are a doctor, type -login"
        border(page, 100)

        # Get user input
        try:
            info.append(take_input("Name: "))
            info.append(take_input("Email: "))
            info.append(take_input("Password: "))
            info.append(take_input("Repeat pasword: "))
        except InfoCommand:
            register_page()
            return
        except RedirectCommand:
            return

        # Extract user information
        name, email, password, confirm = info

        # Validate user information
        if not name:  # name is optional
            name = "User"

        if not email or not password or not confirm:
            print("Missing required input")
            continue

        if password != confirm:
            print("Passwords doesn't match")
            continue

        # Returns None if invalid, normalized email if valid
        email = check_email(email)
        if not email:
            print("Invalid email address")
            continue

        # Input validation went well
        break
    else:
        # Too many registration attempts
        print("Too many attempts, exiting program...")
        return

    # If email is already registered
    with open("patients.csv", "r") as patients_db:
        reader = DictReader(patients_db, fieldnames=[
                            "name", "email", "password"])
        for row in reader:
            if row["email"] == email:
                print("Email already exists, consider logging in instead")
                login_page()
                return

    # Input data into the patients database
    with open("patients.csv", "a", newline="") as patients_db:
        writer = DictWriter(patients_db, fieldnames=[
                            "name", "email", "password"])
        writer.writerow(
            {"name": name, "email": email, "password": password})

    # Registration successful
    print("Account has been registered successfully!")
    home_page()


def login_page():
    print("This is the login page")


def home_page():
    print("This is the home page")


def schedule_page():
    print("This is the schedule page")


def receipts_page():
    print("This is the receipts page")


def reports_page():
    print("This is the reports page")


def receipt_page():
    ...


def report_page():
    ...


if __name__ == "__main__":
    main()

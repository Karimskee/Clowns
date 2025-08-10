"""
Medical appointments system
"""
from csv import DictReader, DictWriter
from datetime import date, timedelta
from email_validator import EmailNotValidError, validate_email
from math import ceil, floor
import os
import sys


# If user typed an informative command (e.g. -help)
class InfoCommand(Exception):
    pass


# If user typed a redirective command (e.g. -login)
class RedirectCommand(Exception):
    pass


session = {}
commands = ["-help", "-login", "-register", "-home",
            "-schedule", "-receipts", "-reports"]


def main():
    clear_terminal()
    login_page()


def register_page():
    """Patient registration page"""
    # Loops till the user successfully registers their account
    while True:
        # [name, email, password, confirm]
        info = []

        # Ask for user information
        page = "Register your account\n"
        page += "If you already have an account or you are a doctor, type -login\n"
        page += "For the list of the program commands, type -help"
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
        name = check_name(name)

        if not check_missing(email, password, confirm):
            print("Missing required input.")
            continue

        # Returns None if invalid, normalized email if valid
        email = check_email(email)
        if not email:
            print("Invalid email address.")
            continue

        if not check_password(password, confirm):
            print("Passwords doesn't match.")
            continue

        # Input validation went well
        break

    # If email is already registered
    with open("users_login.csv", "r") as users_db:
        reader = DictReader(users_db)

        for row in reader:
            if row["email"] == email:
                print("Email already exists, consider logging in instead")
                login_page()
                return

    # Input data into the patients database
    with open("users_login.csv", "a", newline="") as users_db:
        writer = DictWriter(users_db, fieldnames=[
                            "name", "email", "password", "type"])
        writer.writerow(
            {"name": name, "email": email, "password": password, "type": "patient"})

    # Registration successful
    print("Account has been registered successfully!")
    session["email"] = email
    session["name"] = name
    session["type"] = "patient"
    home_page()


def login_page():
    """Patient/doctor login page"""
    # Page UI
    page = "Login to your account\n"
    page += "If you don't have an account, type -register\n"
    page += "For the list of the program commands, type -help"
    border(page, 100)

    # Get user login information
    try:
        email = take_input("Email: ")
        password = take_input("Password: ")
    except InfoCommand:
        login_page()
        return
    except RedirectCommand:
        return

    # Check if the email is registered
    with open("users_login.csv", "r") as file:
        reader = DictReader(file)

        for row in reader:
            if row["email"] == email:
                if row["password"] == password:
                    session["name"] = row["name"]
                    session["email"] = email
                    session["type"] = row["type"]
                    print("Successfully logged in.")
                    home_page()
                    return
                else:
                    print("Incorrect password.")
                    login_page()
                    return

        print("Email not found.")
        login_page()
        return


def home_page():
    """Hospital home page"""
    login_required()

    page = "Clowns hospital\n"
    page += f"how can we serve you today, {session["name"]}?\n"
    page += "1- Schedule an appointment\n"
    page += "2- View your receipts\n"
    page += "3- View your reports\n"
    page += "4- Logout\n"
    page += "5- Close the program"

    border(page, 100)

    try:
        choice = int(take_input("Enter your choice: "))
    except InfoCommand:
        home_page()
        return
    except RedirectCommand:
        return

    if choice == 1:
        schedule_page()
        return
    elif choice == 2:
        receipts_page()
        return
    elif choice == 3:
        reports_page()
        return
    elif choice == 4:
        session.clear()
        login_page()
    elif choice == 5:
        clear_terminal()
        sys.exit()
    else:
        print("Invalid choice.")
        home_page()


def schedule_page():
    """Schedule an appointment with a doctor page"""
    login_required()

    # Page UI
    page = "Schedule an appointment\n"
    page += "-----------------------\n"
    page += "Specializations:"

    # Set of specializations the hospital offers
    specs = set()

    # Get specializations from the database
    with open("doctors_info.csv", "r") as doctors_db:
        reader = DictReader(doctors_db)
        for row in reader:
            specs.add(row["specialization"])

    # Add specializations to the page UI
    specs = list(specs)
    for i in range(len(specs)):
        page += f"\n{i + 1}- {specs[i]}"

    # Print the page UI
    border(page, 100)

    # Get desired specialization number from the user
    try:
        spec_num = int(take_input("Enter the specialization number: "))
    except InfoCommand:
        schedule_page()
        return
    except RedirectCommand:
        return

    # List of doctors with their info in the desired specialization
    doctors = []

    # Get the list of doctors in the desired specialization
    with open("doctors_info.csv", "r") as doctors_db:
        reader = DictReader(doctors_db)
        for row in reader:
            if row["specialization"] == specs[spec_num - 1]:
                row.pop("turn")
                doctors.append(row)

    # Print the available doctors
    for i in range(len(doctors)):
        print(f"{i + 1}- {doctors[i]['name']}")

    # Get desired doctor number from the user
    try:
        doctor_num = int(take_input("Enter the doctor number: "))
    except InfoCommand:
        schedule_page()
        return
    except RedirectCommand:
        return

    # Get desired doctor information
    doctor = doctors[doctor_num - 1]

    # Set the appointment date (currently, your appointment dates are 1 day after your scheduling)
    appointment_date = date.today() + timedelta(days=1)

    # Set the patient turn (1 if doctor has no prior appointments in that day)
    turn = 1

    # Update the turn if prior appointments for the same doctor exist
    with open("schedules.csv", "r") as schedules_db:
        reader = DictReader(schedules_db)
        for row in reader:
            if row["doctor"] == doctor["name"] and row["date"] == str(appointment_date):
                turn = max(turn, int(row["turn"])) + 1

    with open("schedules.csv", "a", newline="") as schedules_db:
        writer = DictWriter(schedules_db,
                            fieldnames=['date', 'doctor', 'turn'])
        writer.writerow({
            "date": appointment_date,
            "doctor": doctor["name"],
            "turn": turn,
        })

    # Add receipt
    with open("receipts.csv", "a", newline="") as receipts_db:
        writer = DictWriter(receipts_db,
                            fieldnames=["patient_email", "doctor_name",
                                        "turn", "cost", "clinic", "date"])
        writer.writerow({
            "patient_email": session["email"],
            "doctor_name": doctor["name"],
            "turn": turn,
            "cost": "$50",
            "clinic": doctor["clinic"],
            "date": str(appointment_date),
        })

    # Add data to reports

    # Successful appointment scheduling
    print("Your appointment has been scheduled successfully!")
    receipts_page()


"""
    with open("filename.csv", "r") as File:
        reader = DictReader(File, fieldnames=[
                            "name", "field2", "password"])
        for row in reader:
            if row["field2"] == field2:

    with open("filename.csv", "a", newline="") as File:
        writer = DictWriter(File, fieldnames=["field1", "field2", "field3"])
        writer.writerow({"field1": field1, "field2": field2, "field3": field3})
"""


def receipts_page():
    """Display all patient receipts"""
    login_required()

    # Page UI
    page = "Your receipts"
    border(page, 100)

    # Variable to store receipts
    patient_receipts = []

    # Get receipts from the database
    with open("receipts.csv", 'r') as file:
        reader = DictReader(file)

        for row in reader:
            if row['patient_email'] == session['email']:
                patient_receipts.append(row)

    # Reverse cronogical order
    patient_receipts.reverse()

    # Print receipts
    if len(patient_receipts):
        for i in range(len(patient_receipts)):
            patient_receipts[i].pop("patient_email")  # Ignore patient_email
            items = list(patient_receipts[i].items())

            print(f"{i + 1}- ", end="")

            for item in items[0: -1]:
                print(f"{item[0]}: {item[1]}, ", end="")
            print(f"{items[-1][0]}: {items[-1][1]}")
    else:
        print("No receipts")

    # Wait for user command
    while True:
        help()

        try:
            take_input("Enter one of these commands: ")
        except (InfoCommand, RedirectCommand):
            return
        else:
            print("Invalid command.")


def reports_page():
    """Display all patient reports"""
    login_required()

    # Page UI
    page = "Your reports"
    border(page, 100)

    # Variable to store reports
    patient_reports = []

    # Get reports from the database
    with open("finished_reports.csv", 'r') as file:
        reader = DictReader(file)

        for row in reader:
            if row['patient_email'] == session['email']:
                patient_reports.append(row)

    # Reverse cronogical order
    patient_reports.reverse()

    # Print reports
    if len(patient_reports):
        for i in range(len(patient_reports)):
            patient_reports[i].pop("patient_email")  # Ignore patient_email
            items = list(patient_reports[i].items())

            print(f"Report #{i + 1}")

            for item in items[0: -1]:
                print(f"{item[0]}: {item[1]}")
            print()
    else:
        print("No reports")

    # Wait for user command
    while True:
        help()

        try:
            take_input("Enter one of these commands: ")
        except (InfoCommand, RedirectCommand):
            return
        else:
            print("Invalid command.")


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def space(n: int):
    """Prints n blank lines"""
    print("\n" * n)
    ...


def border(s: str, size: int = 0):
    """
    Prints a border around the text
    s: string to print
    c: character to use for the border
    """
    # Split s into a list of lines of s
    list = s.splitlines()

    # Get maximum line length for proper border setting (unless size is fixed)
    maxim = 0
    for element in list:
        maxim = max(maxim, len(element))

    if size < maxim:
        size = maxim

    # Print border according to the largest line length
    print("+" + "-" * (size + 2) + "+")  # Border top

    # Border middle
    for i in range(len(list)):
        blank_spaces = ((size + 2) - len(list[i])) / 2

        print("|" + " " * floor(blank_spaces) + list[i] +
                    " " * ceil(blank_spaces) + "|")

    print("+" + "-" * (size + 2) + "+")  # Border bottom


def check_name(name: str):
    """Validates user name"""
    if not name:
        return "User"  # name is optional, default is "User"
    return name


def check_missing(email: str, password: str, confirm: str):
    if not email or not password or not confirm:
        return False
    return True


def check_email(email: str):
    try:
        emailinfo = validate_email(email, check_deliverability=True)
        email = emailinfo.normalized
        return email
    except EmailNotValidError:
        return None


def check_password(password: str, confirm: str):
    if password != confirm:
        return False
    return True


def help():
    print("Commands: ", end="")
    for command in commands:
        print(command, end=" ")
    print()


def run_command(command: str):
    """Executes program commands"""
    from project import register_page, login_page, home_page, schedule_page, receipts_page, reports_page

    # Information commands
    if command == "-help":
        help()
        raise InfoCommand
    # Page redirection commands
    elif command == "-login":
        login_page()
    elif command == "-register":
        register_page()
    elif command == "-home":
        home_page()
    elif command == "-schedule":
        schedule_page()
    elif command == "-receipts":
        receipts_page()
    elif command == "-reports":
        reports_page()
    # Invalid command
    else:
        return False

    raise RedirectCommand


def take_input(s: str):
    """Takes user input while checking for program commands"""
    inpt = input(s).strip()
    run_command(inpt)
    return inpt


def login_required():
    """Checks if the user is logged in to access certain pages"""
    if not session.get("email"):
        print("You must be logged in to access this page.")
        login_page()


if __name__ == "__main__":
    main()

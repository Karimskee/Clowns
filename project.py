"""
Medical appointments system
"""
from email_validator import validate_email, EmailNotValidError
from math import ceil, floor
import os
from csv import DictReader, DictWriter
from datetime import date, timedelta

# If user typed an informative command (e.g. -help)


class InfoCommand(Exception):
    pass

# If user typed a redirective command (e.g. -login)


class RedirectCommand(Exception):
    pass


commands = ["-help", "-login", "-register", "-home",
            "-schedule", "-receipts", "-reports"]


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
        name = check_name(name)

        if not check_missing(email, password, confirm):
            print("Missing required input")
            continue

        # Returns None if invalid, normalized email if valid
        email = check_email(email)
        if not email:
            print("Invalid email address")
            continue

        if not check_password(password, confirm):
            print("Passwords doesn't match")
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
    """Schedule an appointment with a doctor page"""
    # Page UI
    page = "Schedule an appointment\n"
    page += "-----------------------\n"
    page += "Specializations:"

    # Set of specializations the hospital offers
    specs = set()

    # Get specializations from the database
    with open("doctors.csv", "r") as doctors_db:
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
    with open("doctors.csv", "r") as doctors_db:
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
            "patient_email": "dumb@email.com",
            "doctor_name": doctor["name"],
            "turn": turn,
            "cost": "$50",
            "clinic": doctor["clinic"],
            "date": str(appointment_date),
        })

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
    print("This is the receipts page")


def reports_page():
    print("This is the reports page")


def receipt_page():
    ...


def report_page():
    ...


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
    print("Commands:")
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
    inpt = input(s).strip()
    run_command(inpt)
    return inpt


if __name__ == "__main__":
    main()

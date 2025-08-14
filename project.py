"""
Medical appointments system
"""
from csv import DictReader, DictWriter
from datetime import date, timedelta
from email_validator import EmailNotValidError, validate_email
from math import ceil, floor
import os
import sys
import string

# patient session class


class Session:
    def __init__(self, name, email, type):
        self.name = name
        self.email = email
        self.type = type

    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}, Type: {self.type}"

    def check(self):
        if self.type == 'doctor':
            return 'doctor'
        elif self.type == 'patient':
            return 'patient'


# commands class
class Commands(Session):
    doctors = ['-login', '-home', '-receipts',
               '-unfinished', '-finished', '-logout', '-exit']
    patients = ['-help', '-login', '-register', '-home',
                '-schedule', '-receipts', '-reports', '-logout', '-exit']

    def __init__(self, name, email, type):
        super().__init__(name, email, type)
        if self.check() == 'doctor':
            self.commands = self.doctors
        else:
            self.commands = self.patients

    def __str__(self):
        return ", ".join(self.commands)


session = Session()
commands = ["-help", "-login", "-register", "-home",
            "-schedule", "-receipts", "-reports"]


def main():
    clear_terminal()
    login_page()


"""
██████╗  █████╗  ██████╗ ███████╗███████╗
██╔══██╗██╔══██╗██╔════╝ ██╔════╝██╔════╝
██████╔╝███████║██║  ███╗█████╗  ███████╗
██╔═══╝ ██╔══██║██║   ██║██╔══╝  ╚════██║
██║     ██║  ██║╚██████╔╝███████╗███████║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝
"""


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
            # check name has first and last
            while True:
                # input name
                name = take_input("Name: ")

                # check name
                if not check_name_again(name):
                    print("Name should have first and last")
                    continue
                else:
                    if not valid_name(name):
                        print("Not a valid name")
                    else:
                        break

            info.append(name)
            while True:
                # email input
                gmail = take_input("Email: ")
                # Returns None if invalid, normalized email if valid

                email = check_email(gmail)
                if not email:
                    print("Invalid email address.")
                else:
                    email = gmail
                    info.append(email)
                    break

            # Input password while validating its strength
            while True:
                # Input password
                password = take_input("Password: ")

                # Check passwords strength
                if not check_strong_password(password):
                    print(
                        "please enter at least 8 letters, one digit, a sympol, upper and lower character")
                    continue
                else:
                    break

            info.append(password)
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

        if not check_password(password, confirm):
            print("Passwords doesn't match.")
            continue

        # Input validation went well
        break

    # If email is already registered
    with open(r"C:\Users\elhaty\OneDrive - Faculty of Computers & Artificial Intelligence\Documents\GitHub\Clowns\users_login.csv", "r") as users_db:
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
    print(session)  # DEBUG

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
                    session["email"] = row["email"]
                    session["type"] = row["type"]

                    print("Successfully logged in.")

                    if session["type"] == "patient":
                        home_page()
                    else:
                        doctor_page()

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
    print(session)  # DEBUG
    login_required()

    page = "Ducktors hospital\n"
    page += f"how can we serve you today, {session['name']}?\n"
    page += "1- Schedule an appointment\n"
    page += "2- View your receipts\n"
    page += "3- View your reports\n"
    page += "4- Logout\n"
    page += "5- Close the program"

    border(page, 100)
    while True:
        try:
            choice = int(take_input("Enter your choice: "))
            break
        except ValueError or UnboundLocalError:
            print()
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
        logout()
    elif choice == 5:
        clear_terminal()
        sys.exit()
    else:
        print("Invalid choice.")
        home_page()

    return


def schedule_page():
    """Schedule an appointment with a doctor page"""
    print(session)  # DEBUG
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
    while True:
        try:
            spec_num = int(take_input("Enter the specialization number: "))
            break
        except ValueError or UnboundLocalError:
            print()
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
    while True:
        try:
            doctor_num = int(take_input("Enter the doctor number: "))
            break
        except ValueError or UnboundLocalError:
            print()
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
    with open("unfinished_reports.csv", "a", newline="") as file:
        writer = DictWriter(file, fieldnames=[
                            "patient_email", "doctor_name", "date", "turn", "notes"])

        writer.writerow({
            "patient_email": session["email"],
            "doctor_name": doctor["name"],
            "date": str(appointment_date),
            "turn": turn,
            "notes": "",
        })

    # Successful appointment scheduling
    print("Your appointment has been scheduled successfully!")
    receipts_page()


def receipts_page():
    """Display all patient receipts"""
    print(session)  # DEBUG
    login_required()

    # Page UI
    page = "Your receipts"
    border(page, 100)

    # Variable to store receipts
    receipts = []

    # Get receipts from the database
    with open("receipts.csv", 'r') as file:
        reader = DictReader(file)

        for row in reader:
            # Get recipets for a patient or a doctor
            if session["type"] == "patient":
                if row["patient_email"] == session["email"]:
                    receipts.append(row)
            else:
                if row["doctor_name"] == session["name"]:
                    receipts.append(row)

    # Reverse cronogical order
    receipts.reverse()

    # Print receipts
    if len(receipts):
        for i in range(len(receipts)):
            if session["type"] == "patient":
                # Ignore patient_email if patient session
                receipts[i].pop("patient_email")
            else:
                # Ignore doctor_name if doctor session
                receipts[i].pop("doctor_name")

            items = list(receipts[i].items())

            print(f"{i + 1}- ", end="")

            for item in items[0: -1]:
                print(f"{item[0]}: {item[1]}, ", end="")
            print(f"{items[-1][0]}: {items[-1][1]}")
    else:
        print("No receipts")

    print(session)  # DEBUG

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
    reports = []

    # Get reports from the database
    with open("finished_reports.csv", 'r') as file:
        reader = DictReader(file)

        for row in reader:
            # Get reports for a patient or a doctor (finished reports for doctors)
            if session["type"] == "patient":
                if row['patient_email'] == session['email']:
                    reports.append(row)
            else:
                if row['doctor_name'] == session['name']:
                    reports.append(row)

    # Reverse cronogical order
    reports.reverse()

    # Print reports
    if len(reports):
        for i in range(len(reports)):
            if session["type"] == "patient":
                # Ignore patient_email if patient session
                reports[i].pop("patient_email")
            else:
                # Ignore doctor_name if doctor session
                reports[i].pop("doctor_name")

            items = list(reports[i].items())

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


def doctor_page():
    page = f"Welcome back Dr. {session['name']}!\n"
    page += "1- View your receipts\n"
    page += "2- View unfinished reports\n"
    page += "3- View finished reports\n"
    page += "4- Logout"
    border(page, 100)

    while True:
        try:
            choice = int(take_input("Enter your choice: "))
            if 1 <= choice <= 4:
                break
        except ValueError or UnboundLocalError:
            print()

        except (InfoCommand, RedirectCommand):
            return

    if choice == 1:
        receipts_page()
    elif choice == 2:
        unfinished_reports_page()
    elif choice == 3:
        finished_reports_page()
    elif choice == 4:
        logout()
    else:
        print("Invalid command.")
        doctor_page()

    return


def unfinished_reports_page():
    """Display all unfinished reports for the doctor to finish (unfinished_reports.csv)"""
    page = "Unfinished reports\n"
    border(page, 100)

    # Store all doctor's unfinished_reports in a variable
    unfinished = []

    # Search for all rows for a doctor name
    with open("unfinished_reports.csv", 'r') as file:
        reader = DictReader(file)

        for row in reader:
            if row['doctor_name'] == session['name']:
                unfinished.append(row)

    if not len(unfinished):
        print("All reports are finished")

        # Wait for user command
        while True:
            help()

            try:
                take_input("Enter one of these commands: ")
            except (InfoCommand, RedirectCommand):
                return
            else:
                print("Invalid command.")

    # Print doctor's unfinished reports
    for i in range(len(unfinished)):
        unfinished[i].pop("doctor_name")

        items = list(unfinished[i].items())

        print(f"{i + 1}- ", end="")
        for item in items[0: -2]:
            print(f"{item[0]}: {item[1]}, ", end="")
        print(f"{items[-2][0]}: {items[-2][1]}")

    # Get chosen report number
    while True:
        try:
            chosen_number = int(take_input("Report number to finish: "))
            notes = take_input("Notes: ")
            if 1 <= chosen_number <= len(unfinished):
                break
        except ValueError or UnboundLocalError:
            print()
        except InfoCommand:
            unfinished_reports_page()
            return
        except RedirectCommand:
            return

    # Get chosen report
    chosen_report = unfinished[chosen_number - 1]

    # Add back doctor_name which was removed for easier printing process
    chosen_report["doctor_name"] = session["name"]

    # Store the whole unfinished_reports file in a variable (to remove the finished reports)
    all_reports = []

    # Rewrite the unfinished_reports such that it only includes untouched reports
    with open("unfinished_reports.csv", 'r') as file:
        reader = DictReader(file)

        for row in reader:
            if row != chosen_report:
                all_reports.append(row)

    # Add notes after getting all_reports, so the condition is valid
    chosen_report["notes"] = notes

    with open("unfinished_reports.csv", "w", newline="") as file:
        writer = DictWriter(file, fieldnames=[
            "patient_email", "doctor_name", "date", "turn", "notes"])
        writer.writeheader()

        if len(all_reports):
            writer.writerows(all_reports)

    # Append finished report to the finished_reports file
    with open("finished_reports.csv", "a", newline="") as file:
        writer = DictWriter(file, fieldnames=[
            "patient_email", "doctor_name", "date", "turn", "notes"])
        writer.writerow(chosen_report)

    print("Report finished.")
    unfinished_reports_page()


def finished_reports_page():
    """Display all finished reports for the doctor (finished_reports.csv)"""
    page = "Finished reports\n"
    border(page, 100)

    finished = []

    with open("finished_reports.csv", "r") as file:
        reader = DictReader(file)
        finished = list(reader)

    if len(finished):
        for i in range(len(finished)):
            finished[i].pop("doctor_name")

            items = list(finished[i].items())

            print(f"{i + 1}- ", end="")
            for item in items[0: -1]:
                print(f"{item[0]}: {item[1]}, ", end="")
            print(f"{items[-1][0]}: {items[-1][1]}")
    else:
        print("No reports found.")

    # Wait for user command
    while True:
        help()

        try:
            take_input("Enter one of these commands: ")
        except (InfoCommand, RedirectCommand):
            return
        else:
            print("Invalid command.")


"""
██╗  ██╗███████╗██╗     ██████╗ ███████╗██████╗ ███████╗
██║  ██║██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗██╔════╝
███████║█████╗  ██║     ██████╔╝█████╗  ██████╔╝███████╗
██╔══██║██╔══╝  ██║     ██╔═══╝ ██╔══╝  ██╔══██╗╚════██║
██║  ██║███████╗███████╗██║     ███████╗██║  ██║███████║
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝
"""


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

# check password


def check_strong_password(password: str):
    """Checks if the password is strong enough"""
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in string.punctuation for char in password):
        return False

    return True


def check_password(password: str, confirm: str):
    if password != confirm:
        return False
    return True


# count spaces in name
def check_name_again(name: str):
    return name.count(' ') == 1

# check is a valid name


def valid_name(name: str):

    for char in name:
        if char.isdigit():
            return False
        if char in string.punctuation:
            return False

    return True


def help():
    print("Commands: ", end="")
    for command in commands('doctor'):
        print(command, end=" ")
    print()


def run_command(command: str):
    """Executes program commands"""
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


def logout():
    """Clears the session and returns to the login page"""
    session.clear()
    login_page()


if __name__ == "__main__":
    main()

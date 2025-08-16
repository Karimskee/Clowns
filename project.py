"""
Ducktors:
---------
A hospital terminal program for CS50 Python Final Project

Functionalities:
--------------------
For patients: schedule appointments, view self records and doctor reports
For doctors: write reports, view patients records
"""
from colorama import Fore, Style
from csv import DictReader, DictWriter
from datetime import date, timedelta
from email_validator import EmailNotValidError, validate_email
from math import ceil, floor
import os
import pyfiglet
import string
import sys


# If user typed an informative command (e.g. -help)
class InfoCommand(Exception):
    pass


# If user typed a redirective command (e.g. -login)
class RedirectCommand(Exception):
    pass


# As long as the user is logged in, their session memorises their name, email and type
class Session:
    def __init__(self):
        # Values are set on login/register
        self.name = ""
        self.email = ""
        self.type = "" # Whether "patient" or "doctor"

    def __str__(self):
        """For printing user login information"""
        return f"Name: {self.name}, Email: {self.email}, Type: {self.type}"

    def clear(self):
        """Clears all the session values"""
        self.name, self.email, self.type = "", "", ""


# For program specific commands
class Commands(Session):
    def __init__(self):
        self.patients = ['-help', '-login', '-register', '-home',
                         '-schedule', '-receipts', '-reports', '-logout', '-exit']

        self.doctors = ['-login', '-home', '-receipts',
                        '-unfinished', '-finished', '-logout', '-exit']

    # Prints available commands for user (doctor or patient commands)
    def __str__(self):
        output = "\n Commands:\n "

        if session.type == "patient":
            output += ", ".join(self.patients)
        else:
            output += ", ".join(self.doctors)

        output += "\n"
        return output

    # Tries running the command
    # If -help command, print available commands
    # If redirectional commands, redirect to the needed page
    # If invalid_command or not a command at all, warn user
    def run(self, command):
        """Executes program commands"""
        if command.startswith("-"):
            # Information commands
            if command == "-help":
                print(Fore.YELLOW, commands)
                raise InfoCommand
            
            # Page redirection commands
            elif command == "-login":
                login_page()
            elif command == "-register":
                register_page()
            elif command == "-home":
                if session.type == "patient":
                    patients_page()
                else:
                    doctors_page()
            elif command == "-schedule":
                schedule_page()
            elif command == "-receipts":
                receipts_page()
            elif command == "-reports":
                reports_page()
            elif command == "-logout":
                logout()
            elif command == "-exit":
                exit_program()
            elif command == "-unfinished":
                unfinished_reports_page()
            elif command == "-finished":
                finished_reports_page()
            else:
                print(Fore.RED, "Invalid command.")
                return False
            
        # Not a command at all
        else:
            return False
            
        # Page redirection command has been executed
        raise RedirectCommand


session = Session()
commands = Commands()


def main():
    """Beginning of the program"""
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


def login_page():
    """Patient/doctor login page"""
    # Page UI
    ducktors()
    page =  "Log in to your account\n"
    page += "---------------------\n"
    page += "No account? -register\n"
    page += "For program commands: -help"
    border(page)

    # Get user login information
    email = get_email("Email: ")
    password = get_input("Password: ")

    # Check if the email is registered
    with open("datasets/users_login.csv", "r") as file:
        reader = DictReader(file)

        for row in reader:
            if row["email"] == email:
                if row["password"] == password:
                    session.name = row["name"]
                    session.email = row["email"]
                    session.type = row["type"]

                    print(Fore.GREEN, "Successfully logged in.")

                    if session.type == "patient":
                        patients_page()
                    else:
                        doctors_page()

                    return
                else:
                    print(Fore.RED, "Incorrect password.")
                    login_page()
                    return

        print(Fore.RED, "Email not found.")
        login_page()
        return


def register_page():
    """Patient registration page"""
    patient_specific()
    
    # Loops till the user successfully registers their account
    while True:
        info = [] # [name, email, password, confirm]

        # Ask for user information
        print()
        page = "Register your account\n"
        page += "---------------------\n"
        page += "For program commands: -help\n"
        page += "Have an account? -login"
        border(page)

        # Get user input
        # Input name
        info.append(get_name("Name (First & Last): "))

        # Input email
        info.append(get_email("Email: "))

        # Input password while validating its strength
        while True:
            # Input password
            password = get_input("Password: ")

            # Check passwords strength
            if not is_strong_password(password):
                print(Fore.RED,
                    "please enter at least 8 letters, one digit, a sympol, upper and lower character")
            else:
                break
        info.append(password)

        # Input password confirmation
        info.append(get_input("Repeat pasword: "))

        # Extract user information
        name, email, password, confirm = info

        # Validate passwords match
        if not is_match(password, confirm):
            print(Fore.RED, "Passwords doesn't match.")
            continue

        # Input validation went well
        break

    # If email is already registered
    with open("datasets/users_login.csv", "r") as users_db:
        reader = DictReader(users_db)

        for row in reader:
            if row["email"] == email:
                print(Fore.RED, "Email already exists, consider logging in instead")
                login_page()
                return

    # Input data into the patients database
    with open("datasets/users_login.csv", "a", newline="") as users_db:
        writer = DictWriter(users_db, fieldnames=[
                            "name", "email", "password", "type"])
        writer.writerow(
            {"name": name, "email": email, "password": password, "type": "patient"})

    # Registration successful
    print(Fore.GREEN, "Account has been registered successfully!")
    session.email = email
    session.name = name
    session.type = "patient"
    patients_page()


def patients_page():
    """Patients home page"""
    login_required()
    patient_specific()

    # Page UI
    print()
    page = f"Your orders, {session.name}?\n"
    page +=  "--------------" + "-" * len(session.name) + "\n"
    page += "!left 1- Schedule an appointment\n"
    page += "!left 2- View your receipts\n"
    page += "!left 3- View your reports\n"
    page += "!left 4- Logout\n"
    page += "!left 5- Close the program"
    border(page)

    while True:
        try:
            choice = int(get_input("Enter your choice: "))
            break
        except ValueError:
            ...
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
        print(Fore.RED, "Invalid choice.")
        patients_page()

    return


def schedule_page():
    """Schedule an appointment with a doctor page"""
    login_required()
    patient_specific()

    # Page UI
    print()
    page = "Schedule an appointment\n"
    page += "-----------------------\n"
    page += "!left Specializations:"

    # Set of specializations the hospital offers
    specs = set()

    # Get specializations from the database
    with open("datasets/doctors_info.csv", "r") as doctors_db:
        reader = DictReader(doctors_db)
        for row in reader:
            specs.add(row["specialization"])

    # Add specializations to the page UI
    specs = list(sorted(specs)) 
    for i in range(len(specs)):
        page += f"\n!left {i + 1}- {specs[i]}"

    # Print the page UI
    border(page)

    # Get desired specialization number from the user
    while True:
        try:
            spec_num = int(get_input("Enter the specialization number: "))
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
    with open("datasets/doctors_info.csv", "r") as doctors_db:
        reader = DictReader(doctors_db)
        for row in reader:
            if row["specialization"] == specs[spec_num - 1]:
                doctors.append(row)

    # Print the available doctors
    for i in range(len(doctors)):
        print(Fore.BLUE, f"{i + 1}- {doctors[i]['name']}")

    # Get desired doctor number from the user
    while True:
        print()
        try:
            doctor_num = int(get_input("Enter the doctor number: "))
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
    with open("datasets/schedules.csv", "r") as schedules_db:
        reader = DictReader(schedules_db)
        for row in reader:
            if row["doctor"] == doctor["name"] and row["date"] == str(appointment_date):
                turn = max(turn, int(row["turn"])) + 1

    with open("datasets/schedules.csv", "a", newline="") as schedules_db:
        writer = DictWriter(schedules_db,
                            fieldnames=['date', 'doctor', 'turn'])
        writer.writerow({
            "date": appointment_date,
            "doctor": doctor["name"],
            "turn": turn,
        })

    # Add receipt
    with open("datasets/receipts.csv", "a", newline="") as receipts_db:
        writer = DictWriter(receipts_db,
                            fieldnames=["patient_email", "doctor_name",
                                        "turn", "cost", "clinic", "date"])
        writer.writerow({
            "patient_email": session.email,
            "doctor_name": doctor["name"],
            "turn": turn,
            "cost": "$50",
            "clinic": doctor["clinic"],
            "date": str(appointment_date),
        })

    # Add data to reports
    with open("datasets/unfinished_reports.csv", "a", newline="") as file:
        writer = DictWriter(file, fieldnames=[
                            "patient_email", "doctor_name", "date", "turn", "notes"])

        writer.writerow({
            "patient_email": session.email,
            "doctor_name": doctor["name"],
            "date": str(appointment_date),
            "turn": turn,
            "notes": "",
        })

    # Successful appointment scheduling
    print(Fore.GREEN, "Your appointment has been scheduled successfully!")
    receipts_page()


def receipts_page():
    """Display all patient receipts"""
    login_required()

    # Page UI
    print()
    page = "Your receipts"
    border(page)

    # Variable to store receipts
    receipts = []

    # Get receipts from the database
    with open("datasets/receipts.csv", 'r') as file:
        reader = DictReader(file)

        for row in reader:
            # Get recipets for a patient or a doctor
            if session.type == "patient":
                if row["patient_email"] == session.email:
                    receipts.append(row)
            else:
                if row["doctor_name"] == session.name:
                    receipts.append(row)

    # Reverse cronogical order
    receipts.reverse()

    # Print receipts
    if len(receipts):
        for i in range(len(receipts)):
            if session.type == "patient":
                # Ignore patient_email if patient session
                receipts[i].pop("patient_email")
            else:
                # Ignore doctor_name if doctor session
                receipts[i].pop("doctor_name")

            items = list(receipts[i].items())

            print(Fore.MAGENTA, f"{i + 1}- ", end="")

            for item in items[0: -1]:
                print(f"{item[0]}: {item[1]}, ", end="")
            print(f"{items[-1][0]}: {items[-1][1]}")
    else:
        print(Fore.RED, "No receipts")

    # Wait for user command
    while True:
        print()
        try:
            get_input("Enter a program command (-help for commands): ")
        except InfoCommand:
            continue
        except RedirectCommand:
            return
        else:
            print(Fore.RED, "Invalid command.")


def reports_page():
    """Display all patient reports"""
    login_required()
    patient_specific()

    # Page UI
    print()
    page = "Your reports"
    border(page)

    # Variable to store reports
    reports = []

    # Get reports from the database
    with open("datasets/finished_reports.csv", 'r') as file:
        reader = DictReader(file)

        for row in reader:
            # Get reports for a patient or a doctor (finished reports for doctors)
            if session.type == "patient":
                if row['patient_email'] == session.email:
                    reports.append(row)
            else:
                if row['doctor_name'] == session.name:
                    reports.append(row)

    # Reverse cronogical order
    reports.reverse()

    # Print reports
    if len(reports):
        for i in range(len(reports)):
            if session.type == "patient":
                # Ignore patient_email if patient session
                reports[i].pop("patient_email")
            else:
                # Ignore doctor_name if doctor session
                reports[i].pop("doctor_name")

            items = list(reports[i].items())

            print(Fore.MAGENTA, f"Report #{i + 1}")

            for item in items:
                print(f"{item[0]}: {item[1]}")
            print()
    else:
        print(Fore.RED, "No reports")

    # Wait for user command
    while True:
        print()
        try:
            get_input("Enter a program command (-help for commands): ")
        except InfoCommand:
            continue
        except RedirectCommand:
            return
        else:
            print(Fore.RED, "Invalid command.")


def doctors_page():
    """Doctors home page"""
    login_required()
    doctor_specific()

    # Page UI
    print()
    page = f"Welcome back Dr. {session.name}!\n"
    page += "1- View your receipts\n"
    page += "2- View unfinished reports\n"
    page += "3- View finished reports\n"
    page += "4- Logout"
    border(page)

    while True:
        try:
            choice = int(get_input("Enter your choice: "))
            if 1 <= choice <= 4:
                break
        except ValueError:
            ...
        except RedirectCommand:
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
        print(Fore.RED, "Invalid command.")
        doctors_page()

    return


def unfinished_reports_page():
    """Display all unfinished reports for the doctor to finish (unfinished_reports.csv)"""
    login_required()
    doctor_specific()
    
    # Page UI
    print()
    page = "Unfinished reports\n"
    border(page)

    # Store all doctor's unfinished_reports in a variable
    unfinished = []

    # Search for all rows for a doctor name
    with open("datasets/unfinished_reports.csv", 'r') as file:
        reader = DictReader(file)

        for row in reader:
            if row['doctor_name'] == session.name:
                unfinished.append(row)

    if not len(unfinished):
        print(Fore.GREEN, "All reports are finished!")

        # Wait for user command
        while True:
            print()
            try:
                get_input("Enter a program command (-help for commands): ")
            except InfoCommand:
                continue
            except RedirectCommand:
                return
            else:
                print(Fore.RED, "Invalid command.")

    # Print doctor's unfinished reports
    for i in range(len(unfinished)):
        unfinished[i].pop("doctor_name")

        items = list(unfinished[i].items())

        print(Fore.MAGENTA, f"{i + 1}- ", end="")
        for item in items[0: -2]:
            print(f"{item[0]}: {item[1]}, ", end="")
        print(f"{items[-2][0]}: {items[-2][1]}")

    # Get chosen report number
    while True:
        print()
        try:
            chosen_number = int(get_input("Report number to finish: "))
            notes = get_input("Notes: ")
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
    chosen_report["doctor_name"] = session.name

    # Store the whole unfinished_reports file in a variable (to remove the finished reports)
    all_reports = []

    # Rewrite the unfinished_reports such that it only includes untouched reports
    with open("datasets/unfinished_reports.csv", 'r') as file:
        reader = DictReader(file)

        for row in reader:
            if row != chosen_report:
                all_reports.append(row)

    # Add notes after getting all_reports, so the condition is valid
    chosen_report["notes"] = notes

    with open("datasets/unfinished_reports.csv", "w", newline="") as file:
        writer = DictWriter(file, fieldnames=[
            "patient_email", "doctor_name", "date", "turn", "notes"])
        writer.writeheader()

        if len(all_reports):
            writer.writerows(all_reports)

    # Append finished report to the finished_reports file
    with open("datasets/finished_reports.csv", "a", newline="") as file:
        writer = DictWriter(file, fieldnames=[
            "patient_email", "doctor_name", "date", "turn", "notes"])
        writer.writerow(chosen_report)

    print(Fore.GREEN, "Report finished.")
    unfinished_reports_page()


def finished_reports_page():
    """Display all finished reports for the doctor (finished_reports.csv)"""
    login_required()
    doctor_specific()
    
    # Page UI
    print()
    page = "Finished reports\n"
    border(page)

    finished = []

    with open("datasets/finished_reports.csv", "r") as file:
        reader = DictReader(file)
        finished = list(reader)

    if len(finished):
        for i in range(len(finished)):
            finished[i].pop("doctor_name")

            items = list(finished[i].items())

            print(Fore.MAGENTA, f"{i + 1}- ", end="")
            for item in items[0: -1]:
                print(f"{item[0]}: {item[1]}, ", end="")
            print(f"{items[-1][0]}: {items[-1][1]}")
    else:
        print(Fore.RED, "No reports found.")

    # Wait for user command
    while True:
        print()
        print(Fore.YELLOW, commands)

        try:
            get_input("Enter one of these commands: ")
        except RedirectCommand:
            return
        else:
            print(Fore.RED, "Invalid command.")


"""
██╗  ██╗███████╗██╗     ██████╗ ███████╗██████╗ ███████╗
██║  ██║██╔════╝██║     ██╔══██╗██╔════╝██╔══██╗██╔════╝
███████║█████╗  ██║     ██████╔╝█████╗  ██████╔╝███████╗
██╔══██║██╔══╝  ██║     ██╔═══╝ ██╔══╝  ██╔══██╗╚════██║
██║  ██║███████╗███████╗██║     ███████╗██║  ██║███████║
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝
"""


def ducktors():
    """Print ASCII Art of Ducktors Hospital"""
    print()
    ducktors = "Ducktors Hospital"
    print(Fore.YELLOW + Style.BRIGHT + pyfiglet.figlet_format(ducktors, width=200, font="ansi_shadow", justify="left"), end="")


def clear_terminal():
    """Clears the terminal for better UI"""
    os.system('cls' if os.name == 'nt' else 'clear')


def space(n: int):
    """Prints n blank lines"""
    print("\n" * n)
    ...


def border(s: str, size: int = 128):
    """
    Prints a border around the text
    """
    # Split s into a list of lines of s
    lines = s.splitlines()

    # Get maximum line length for proper border setting (unless size is fixed)
    maxim = 0
    for line in lines:
        maxim = max(maxim, len(line))

    if size < maxim:
        size = maxim

    # Print border according to the largest line length
    print(Fore.WHITE, "+" + "-" * (size + 2) + "+")  # Border top

    # Border middle
    for line in lines:
        # The number of spaces whether on the left or right if text is centered
        blank_spaces = ((size + 2) - len(line)) / 2

        if line.startswith("!left "):
            line = line.removeprefix("!left ")
            print(Fore.WHITE, "|" + " " + line + " " * floor(blank_spaces * 2 + 5) + "|")

        elif line.startswith("!right "):
            line = line.removeprefix("!right ")
            print(Fore.WHITE, "|" + " " * floor(blank_spaces * 2 + 6) + line + " " + "|")

        else:
            print(Fore.WHITE, "|" + " " * floor(blank_spaces) + line + " " * ceil(blank_spaces) + "|")

    print(Fore.WHITE, "+" + "-" * (size + 2) + "+")  # Border bottom
    print()


def is_email(email: str):
    """Validate email address"""
    try:
        emailinfo = validate_email(email, check_deliverability=True)
        email = emailinfo.normalized
    except EmailNotValidError:
        return False
    
    return True


# Check password
def is_strong_password(password: str):
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


def is_match(password: str, confirm: str):
    """If passwords match"""
    if password != confirm:
        return False
    return True


# check is a valid name
def is_valid_name(name: str):
    """
    If name is valid
    Rules:
    1- First and last name separated by a space
    2- Only alphabetical characters
    """
    spaces = name.count(' ')  # count spaces

    if not name:
        return " " + Fore.CYAN + "Name (First & Last): "

    if spaces != 1:
        return " " + Fore.RED + "Format: First_Name Last_Name."

    if any(char.isdigit() for char in name) or \
            any(char in string.punctuation for char in name):
        return " " + Fore.RED + "Invalid name, only alphabetical characters allowed."

    return True


def is_command(s: str):
    """Checks if the user has entered a program command"""
    try:
        commands.run(s)
    except InfoCommand:
        raise InfoCommand
    except RedirectCommand:
        raise RedirectCommand
    
    return False


def get_name(s: str):
    """Inputs and validates user name"""
    while True:
        inpt = input(Fore.BLUE + " " + s).strip()
        
        if not inpt:
           continue
        
        if is_command(inpt):
            return

        # Validate name
        result = is_valid_name(inpt)
        if result == True:
            break
        else:
            print(result)

    return inpt


def get_email(s: str):
    """Inputs and validates user email"""
    print(Fore.BLUE, end="")
    while True:
        inpt = input(Fore.BLUE + " " + s).strip()
        
        if not inpt:
           continue

        if is_command(inpt):
            return

        # Validate email
        if is_email(inpt):
            break
        else:
            print(Fore.RED, "Invalid email address.")

    print(Fore.WHITE, end="")
    return inpt


def get_input(s: str):
    """Get user input while checking for program commands"""
    while True:
        inpt = input(Fore.BLUE + " " + s).strip()
        
        try:
            is_command(inpt)
        except InfoCommand:
            raise InfoCommand
        except RedirectCommand:
            raise RedirectCommand
        
        if input:
            break

    print(Fore.WHITE, end="")
    return inpt


def login_required():
    """Checks if the user is logged in to access certain pages"""
    if not session.email:
        print(Fore.RED, "You must be logged in to access this page.")
        login_page()


def patient_specific():
    """Checks if the user is a patient to access the current page"""
    if session.type != "patient" and session.type != "":
        print(Fore.RED, "This page is a patient specific page, please login with a patient account instead.")
        login_page()


def doctor_specific():
    """Checks if the user is a doctor to access the current page"""
    if session.type != "doctor":
        print(Fore.RED, "This page is a doctor specific page, please login with a doctor account instead.")
        login_page()

def logout():
    """Clears the session and returns to the login page"""
    session.clear()
    print(Fore.GREEN, Style.BRIGHT + "Successfully logged out.")
    login_page()


def exit_program():
    """Clears the terminal and exits the program"""
    clear_terminal()
    print(Fore.WHITE)
    sys.exit()


if __name__ == "__main__":
    main()

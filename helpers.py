from email_validator import validate_email, EmailNotValidError
from math import ceil, floor
import os
import sys
from csv import DictReader, DictWriter


# If user typed an informative command (e.g. -help)
class InfoCommand(Exception):
    pass

# If user typed a redirective command (e.g. -login)


class RedirectCommand(Exception):
    pass


commands = ["-help", "-login", "-register", "-home",
            "-schedule", "-receipts", "-reports"]


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


def check_email(email: str):
    try:
        emailinfo = validate_email(email, check_deliverability=True)
        email = emailinfo.normalized
        return email
    except EmailNotValidError:
        return None


def run_command(command: str):
    """Executes program commands"""
    from project import register_page, login_page, home_page, schedule_page, receipts_page, reports_page

    # Information commands
    if command == "-help":
        print("Commands:")
        for command in commands:
            print(command, end=" ")
            print()
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

"""
Test units for project.py
"""
from colorama import Fore
from project import is_email, is_match, is_strong_password, is_valid_name


def test_is_email():
    # no email ("Invalid email address")
    assert is_email("basmala.com") == False
    assert is_email("basmala@gmail") == False
    assert is_email("basmala@.com") == False
    assert is_email("helloworld") == False
    assert is_email("basmala@") == False
    assert is_email("basmala@com") == False

    # valid emails
    assert is_email("basmala@gmail.com") == True
    assert is_email("rahmatia@gmail.com") == True
    assert is_email("hudamr@gmail.com") == True
    assert is_email("harrypoter@gmail.com") == True
    assert is_email("karimghazy@gmail.com") == True
    assert is_email("saman@gmail.com") == True


def test_is_match():
    # repeat password doesn't match
    assert is_match("Basmala", "Rahma") == False
    assert is_match("Basmala_123", "Rahma_456") == False
    assert is_match("Huda_789", "Karim_101") == False
    assert is_match("Mohamed@112", "Ali#123") == False
    assert is_match("Sara$456", "#Omar%789") == False
    assert is_match("Basmala", "Basmala_123") == False
    assert is_match("Rahma", "Rahma_456") == False
    assert is_match("Huda", "Huda_789") == False

    # repeat password matches
    assert is_match("Basmala_123", "Basmala_123") == True
    assert is_match("Rahma_456", "Rahma_456") == True
    assert is_match("Huda_789", "Huda_789") == True
    assert is_match("Karim_101", "Karim_101") == True
    assert is_match("Mohamed@112", "Mohamed@112") == True
    assert is_match("Ali#123", "Ali#123") == True
    assert is_match("Sara$456", "Sara$456") == True
    assert is_match("#Omar%789", "#Omar%789") == True


def test_is_strong_password():
    # weak password
    assert is_strong_password("") == False
    assert is_strong_password("Basmla") == False
    assert is_strong_password("Rahmatia_") == False
    assert is_strong_password("rahma_1") == False
    assert is_strong_password("Basmala1") == False
    assert is_strong_password("Basmala#") == False
    assert is_strong_password("_basmala1") == False


    # strong password
    assert is_strong_password("Basmala1_") == True
    assert is_strong_password("Bismillah+1") == True
    assert is_strong_password("Basmala#1") == True 
    assert is_strong_password("#Rahmaaaaa0") == True
    assert is_strong_password("#Rah00miii") == True
    assert is_strong_password("Pa ss12!") == True


def test_is_valid_name():
    # name should not be empty
    assert is_valid_name("") == " " + Fore.CYAN + "Name (First & Last): "

    # name should have first and last name
    assert is_valid_name("basmala") == " " + Fore.RED + "Format: First_Name Last_Name."
    assert is_valid_name("basmalarahma") == " " + Fore.RED + "Format: First_Name Last_Name."
    assert is_valid_name("CS50") == " " + Fore.RED + "Format: First_Name Last_Name."
    assert is_valid_name("Basmala Rahma 123") == " " + Fore.RED + "Format: First_Name Last_Name."
    assert is_valid_name("BasmalaRahma@") == " " + Fore.RED + "Format: First_Name Last_Name."
    assert is_valid_name("a b c d e") == " " + Fore.RED + "Format: First_Name Last_Name."

    # name should have only alphabetical characters
    assert is_valid_name(
        "#Basmala Rahma") == " " + Fore.RED + "Invalid name, only alphabetical characters allowed."
    assert is_valid_name(
        "Basmala Rahma@") == " " + Fore.RED + "Invalid name, only alphabetical characters allowed."
    assert is_valid_name(
        "Basmala Rahma123") == " " + Fore.RED + "Invalid name, only alphabetical characters allowed."
    assert is_valid_name(
        "Basmala 444!") == " " + Fore.RED + "Invalid name, only alphabetical characters allowed."
    assert is_valid_name(
        "Basmala Rahma#") == " " + Fore.RED + "Invalid name, only alphabetical characters allowed."
    assert is_valid_name(
        "Basmala Rahma$") == " " + Fore.RED + "Invalid name, only alphabetical characters allowed."
    assert is_valid_name(
        "Basmala Rahma%") == " " + Fore.RED + "Invalid name, only alphabetical characters allowed."

    # Valid names
    assert is_valid_name("Rahma Atia") == True
    assert is_valid_name("Basmala Moahamed") == True
    assert is_valid_name("Huda Amr") == True
    assert is_valid_name("Karim Ghazy") == True
    assert is_valid_name("Mohamed Ali") == True
    assert is_valid_name("Sara Omar") == True
    assert is_valid_name("Wi U") == True

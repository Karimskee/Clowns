from math import ceil, floor


class Doctors:
    Cardiology = [
        {"name": "Basmala Mohamed", "age": 33, "experience": 10, "clinic": "A"},
        {"name": "Ahmed Adel", "age": 30, "experience":  7, "clinic": "B"},
        {"name": "Alaa Abdelnaser", "age": 27, "experience": 5, "clinic": "C"},
    ]

    Neurology = [
        {"name": "Rahma Atia", "age": 25, "experience": 2, "clinic": "D"},
        {"name": "Mohamed Sharkawy", "age": 26, "experience": 3, "clinic": "E"},
        {"name": "Adel Saied", "age": 44, "experience": 20, "clinic": "F"},
    ]

    Orthopedics = [
        {"name": "Mostafa Sameh", "age": 28, "experience": 4, "clinic": "G"},
        {"name": "Mohammed Yassin", "age": 32, "experience": 7, "clinic": "H"},
        {"name": "Anas Ahmed", "age": 41, "experience": 12, "clinic": "I"},
    ]

    Pediatrics = [
        {"name": "Samaa Ahmed", "age": 22, "experience": 1, "clinic": "J"},
        {"name": "Maha Ebrahim", "age": 36, "experience": 13, "clinic": "K"},
        {"name": "Karim Ghazy", "age": 39, "experience": 15, "clinic": "L"},
    ]

    Dermatology = [
        {"name": "Eman Kamal", "age": 34, "experience": 11, "clinic": "M"},
        {"name": "Huda Amr", "age": 37, "experience": 113, "clinic": "N"},
        {"name": "Omar Mahmoud", "age": 44, "experience": 22, "clinic": "O"},
    ]

    def __init__(self, list):
        ...


def set_doctor(n):
    if n == 1:
        print()
    if n == 2:
        print()
    if n == 3:
        print()
    if n == 4:
        print()
    if n == 5:
        print()


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


def ghaseel_mawa3een():
    ...

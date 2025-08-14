from csv import DictReader


# patient session class
class Session:
    def __init__(self):
        self.name = ""
        self.email = ""
        self.type = ""

    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}, Type: {self.type}"


class Commands(Session):

    def __init__(self):
        self.patients = ['-help', '-login', '-register', '-home',
                         '-schedule', '-receipts', '-reports', '-logout', '-exit']

        self.doctors = ['-login', '-home', '-receipts',
                        '-unfinished', '-finished', '-logout', '-exit']

    def __str__(self):
        output = "Commands:\n"

        if session.type == "patient":
            output += ", ".join(self.patients)
        else:
            output += ", ".join(self.doctors)

        output += "\n"
        return output


session = Session()
session.type = "patient"
commands = Commands()

print(commands)

from csv import DictReader

with open("finished_reports.csv", "r") as file:
    reader = DictReader(file)

    print(list(reader))

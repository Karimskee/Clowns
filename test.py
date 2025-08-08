from datetime import date, timedelta
from csv import DictReader
import csv
from helpers import *


def save(doctor, date, turn, doctor_choice):
    turn[doctor_choice] += 1
    current_turn = turn[doctor_choice]
    with open("doctors.txt", "a") as file:
        file.write(
            f"Your Doctor Info : \n"
            f"   Name : {doctor['name']}\n"
            f"   Age : {doctor['age']}\n"
            f"   Experience : {doctor['experience']}\n"
            f"   Clinic : {doctor['clinic']}\n"
            f"Date of appointment : {date} \n"
            f"Your turn is : {current_turn}\n\n"
        )


def main():
    email = "basmala@gmail.com"

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
        doc_choice = int(take_input("Enter the doctor number: "))
    except InfoCommand:
        return
    except RedirectCommand:
        return

    # # Print the available doctors
    # for i in range(len(doctors)):
    #     print(f"{i + 1}- ", end="")
    #     # So that we can subscript the doctor elements
    #     items = list(doctors[i].items())

    #     # Print all doctor elements except the last one
    #     for item in items[: -1]:
    #         print(f"{item[0]}: {item[1]}", end=", ")

    #     # Print the last doctor element
    #     last_item = items[-1]
    #     print(f"{last_item[0]}: {last_item[1]}")

    # update turns
    if 1 <= doc_choice <= 3:
        dates = date.today() + timedelta(days=1)
        # doctor name
        doctor = doctors[doc_choice - 1]['name']
        # patient turn
        turn = 1
        clinic = 'A'
        cost = "$50"
        update_row = []
        last_date = dates
        all_dates = []

        # make all turns 0 in start of the next day
        with open("schedules.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                all_dates.append(row['date'])
            last_date = max(all_dates)

        if last_date != dates:
            with open("schedules.csv", 'a') as file:
                writer = csv.DictWriter(file, fieldnames=[
                                        'date', 'doctor', 'turn'])
            writer.writerow([date, doctor, '1'])

        # update all turns in doctors file
        with open("doctors.csv", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['name'] == doctor:
                    turn = int(row['turn']) + 1
                    row['turn'] = str(turn)
                update_row.append(row)

        with open("doctors.csv", 'w', newline='') as file:
            fieldnames = ['name', 'age', 'experience',
                          'clinic', 'specialization', 'turn']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(update_row)

        with open("schedules.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([dates, doctor, turn])

        with open("doctors.csv", 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['name'] == doctor:
                    clinic = row['clinic']

        with open("receipts.csv", 'a') as file:
            writer = csv.writer(file)
            writer.writerow([email, doctor, turn, cost, clinic, dates])

            # constant cost (50$)
        print("Your appointment has been booked.")
    else:
        print("Invalid doctor choice!")


# patient_email, doctor_name, turn, cost, clinic, date

if __name__ == "__main__":
    main()

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

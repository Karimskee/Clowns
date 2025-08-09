from datetime import date, timedelta
from csv import DictReader
import csv
from helpers import *


# def save(doctor, date, turn, doctor_choice):
#     turn[doctor_choice] += 1
#     current_turn = turn[doctor_choice]
#     with open("doctors.txt", "a") as file:
#         file.write(
#             f"Your Doctor Info : \n"
#             f"   Name : {doctor['name']}\n"
#             f"   Age : {doctor['age']}\n"
#             f"   Experience : {doctor['experience']}\n"
#             f"   Clinic : {doctor['clinic']}\n"
#             f"Date of appointment : {date} \n"
#             f"Your turn is : {current_turn}\n\n"
#         )


def main():
    # email = "basmala@gmail.com"
    finished_reports()

    #     """Schedule an appointment with a doctor page"""
    #     # Page UI
    #     page = "Schedule an appointment\n"
    #     page += "-----------------------\n"
    #     page += "Specializations:"

    #     # Set of specializations the hospital offers
    #     specs = set()

    #     # Get specializations from the database
    #     with open("doctors_info.csv", "r") as doctors_db:
    #         reader = DictReader(doctors_db)
    #         for row in reader:
    #             specs.add(row["specialization"])

    #     # Add specializations to the page UI
    #     specs = list(specs)
    #     for i in range(len(specs)):
    #         page += f"\n{i + 1}- {specs[i]}"

    #     # Print the page UI
    #     border(page, 100)

    #     # Get desired specialization number from the user
    #     try:
    #         spec_num = int(take_input("Enter the specialization number: "))
    #     except InfoCommand:
    #         return
    #     except RedirectCommand:
    #         return

    #     # List of doctors with their info in the desired specialization
    #     doctors = []

    #     # Get the list of doctors in the desired specialization
    #     with open("doctors_info.csv", "r") as doctors_db:
    #         reader = DictReader(doctors_db)
    #         for row in reader:
    #             if row["specialization"] == specs[spec_num - 1]:
    #                 row.pop("turn")
    #                 doctors.append(row)

    #     # Print the available doctors
    #     for i in range(len(doctors)):
    #         print(f"{i + 1}- {doctors[i]['name']}")

    #     # Get desired doctor number from the user
    #     try:
    #         doc_choice = int(take_input("Enter the doctor number: "))
    #     except InfoCommand:
    #         return
    #     except RedirectCommand:
    #         return

    #     # # Print the available doctors
    #     # for i in range(len(doctors)):
    #     #     print(f"{i + 1}- ", end="")
    #     #     # So that we can subscript the doctor elements
    #     #     items = list(doctors[i].items())

    #     #     # Print all doctor elements except the last one
    #     #     for item in items[: -1]:
    #     #         print(f"{item[0]}: {item[1]}", end=", ")

    #     #     # Print the last doctor element
    #     #     last_item = items[-1]
    #     #     print(f"{last_item[0]}: {last_item[1]}")

    #     # update turns
    #     if 1 <= doc_choice <= 3:
    #         dates = date.today() + timedelta(days=1)
    #         # doctor name
    #         doctor = doctors[doc_choice - 1]['name']
    #         # patient turn
    #         turn = 1
    #         clinic = 'A'
    #         cost = "$50"
    #         update_row = []
    #         last_date = dates
    #         all_dates = []

    #         # make all turns 0 in start of the next day
    #         with open("schedules.csv") as file:
    #             reader = csv.DictReader(file)
    #             for row in reader:
    #                 all_dates.append(row['date'])
    #             last_date = max(all_dates)

    #         if last_date != dates:
    #             with open("schedules.csv", 'a') as file:
    #                 writer = csv.DictWriter(file, fieldnames=[
    #                                         'date', 'doctor', 'turn'])
    #             writer.writerow([date, doctor, '1'])

    #         # update all turns in doctors file
    #         with open("doctors_info.csv", newline='') as file:
    #             reader = csv.DictReader(file)
    #             for row in reader:
    #                 if row['name'] == doctor:
    #                     turn = int(row['turn']) + 1
    #                     row['turn'] = str(turn)
    #                 update_row.append(row)

    #         with open("doctors_info.csv", 'w', newline='') as file:
    #             fieldnames = ['name', 'age', 'experience',
    #                           'clinic', 'specialization', 'turn']
    #             writer = csv.DictWriter(file, fieldnames=fieldnames)
    #             writer.writeheader()
    #             writer.writerows(update_row)

    #         with open("schedules.csv", 'a', newline='') as file:
    #             writer = csv.writer(file)
    #             writer.writerow([dates, doctor, turn])

    #         with open("doctors_info.csv", 'r') as file:
    #             reader = csv.DictReader(file)
    #             for row in reader:
    #                 if row['name'] == doctor:
    #                     clinic = row['clinic']

    #         with open("receipts.csv", 'a') as file:
    #             writer = csv.writer(file)
    #             writer.writerow([email, doctor, turn, cost, clinic, dates])

    #             # constant cost (50$)
    #         print("Your appointment has been booked.")
    #     else:
    #         print("Invalid doctor choice!")

    # patient_email, doctor_name, turn, cost, clinic, date

    # receipts page

    # def get_receipts(email="dumb@email.com"):
    #     patient_receipts = []

    #     with open("receipts.csv", 'r') as file:
    #         reader = csv.DictReader(file)
    #         for row in reader:
    #             if row['patient_email'] == email:
    #                 patient_receipts.append(row)

    #     if len(patient_receipts):
    #         for i in range(len(patient_receipts)):
    #             patient_receipts[i].pop("patient_email")
    #             items = list(patient_receipts[i].items())

    #             print(f"{i + 1}- ", end="")

    #             for item in items[0: -1]:
    #                 print(f"{item[0]}: {item[1]}, ", end="")
    #             print(f"{items[-1][0]}: {items[-1][1]}")
    #     else:
    #         print("No receipts")


# Store all doctor's unfinished_reports in a variable
unfinished = []


def finished_reports(doctor_email="basmala@gmail.com"):
    # Search for all rows for a doctor email
    with open("unfinished_reports.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['doctor_email'] == doctor_email:
                unfinished.append(row)

    # Show these rows to the doctor (Karimskee's)
    if len(unfinished):
        choose_report_to_finish()
        add_finished()
    else:
        print("All reports are finished")


# Get the doctor to choose which report to finish (Karimskee's)
chosen = []


def choose_report_to_finish():
    for i in range(len(unfinished)):
        unfinished[i].pop("doctor_email")
        items = list(unfinished[i].items())
    print(f"{i + 1}- ", end="")
    for item in items[0: -1]:
        print(f"{item[0]}: {item[1]}, ", end="")
    print(f"{items[-1][0]}: {items[-1][1]}")
    chosen_one = int(input("Chosen report ?"))
    unfinished[chosen_one - 1]["doctor_notes"] = input("Notes: ")
    chosen.append(unfinished[chosen_one - 1])

    # Get the doctor to type the report note (Karimskee's)

    # Store the whole unfinished_reports file in a variable
    all_reports = []

    # Rewrite the unfinished_reports such that it only includes untouched reports
    with open("unfinished_reports.csv", 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if not row in chosen:
                all_reports.append(row)

    if len(all_reports):
        with open("unfinished_reports.csv", "w", newline="") as File:
            writer = csv.DictWriter(File, fieldnames=[
                                    "patient_email", "doctor_email", "date", "turn", "doctor_notes"])
            writer.writerows(all_reports)

    # Append finished reports to the finished_reports file


def add_finished():
    with open("finished_reports.csv", "a", newline="") as File:
        writer = csv.DictWriter(File, fieldnames=[
                                "patient_email", "doctor_email", "date", "turn", "doctor_notes"])
        writer.writerows(chosen)


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

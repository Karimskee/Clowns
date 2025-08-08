from datetime import date, timedelta
import csv


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
    print(1, "Cardiology")
    print(2, "Neurology")
    print(3, "Orthopedics")
    print(4, "Pediatrics")
    print(5, "Dermatology")

    spec = int(input("Enter a a num ?"))
    print("Doctors in this specialization:")

    """
    doctors =
    [{'number': 1, 'name': ' Rahma Atia'},
    {'number': 2, 'name': ' Mohammed Sharkawy'},
    {'number': 3, 'name': ' Adel Sayed'}]
    """
    doctors = []

    # Get doctors from the database
    with open("doctors.csv", 'r') as file:
        reader = csv.DictReader(file)
        i = 1  # Counter

        # For each line, if found needed specialization, add the doctor
        for line in reader:
            if line["spec"] == str(spec):
                # name,age,experience,clinic
                doctor = {
                    "name": line["name"], "age": line["age"],
                    "experience": line["experience"], "clinic": line["clinic"],
                }
                doctors.append(doctor)
                i += 1

    # Print the available doctors
    for i in range(len(doctors)):
        print(f"{i + 1}- ", end="")
        # So that we can subscript the doctor elements
        items = list(doctors[i].items())

        # Print all doctor elements except the last one
        for item in items[: -1]:
            print(f"{item[0]}: {item[1]}", end=", ")

        # Print the last doctor element
        last_item = items[-1]
        print(f"{last_item[0]}: {last_item[1]}")

    doc_choice = int(input("Your choice is? "))

    if 1 <= doc_choice <= 3:
        dates = date.today() + timedelta(days=1)
        doctor = doctors[doc_choice - 1]['name']
        turn = 1
        update_row = []
        with open("doctors.csv", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['name'] == doctor:
                    turn = int(row['turn']) + 1
                    row['turn'] = str(turn)
                update_row.append(row)

        with open("doctors.csv", 'w', newline='') as file:
            fieldnames = ['spec', 'name', 'age', 'experience',
                          'clinic', 'specialization', 'turn']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(update_row)

        with open("scheudles.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([dates, doctor, turn])

        print("Your appointment has been booked.")
    else:
        print("Invalid doctor choice!")


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

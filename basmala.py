from project import valid_name


# check name has first and last
while True:
    # input name
    name = input("Name: ")

    # check name
    if valid_name(name):
        break
    else:
        valid_name(name)

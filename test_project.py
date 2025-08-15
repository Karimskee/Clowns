from project import is_missing, is_email, is_match, is_valid_name,is_strong_password  


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


def test_is_valid_name():

    # name should not be empty
    assert is_valid_name("") == "Name: "

    # name should have first and last name
    assert is_valid_name("basmala") == "Format: First_Name Last_Name."
    assert is_valid_name("basmalarahma") == "Format: First_Name Last_Name."
    assert is_valid_name("CS50") == "Format: First_Name Last_Name."
    assert is_valid_name("Basmala Rahma 123") == "Format: First_Name Last_Name."
    assert is_valid_name("BasmalaRahma@") == "Format: First_Name Last_Name."
    assert is_valid_name("a b c d e") == "Format: First_Name Last_Name."

    # name should have only alphabetical characters
    assert is_valid_name(
        "#Basmala Rahma") == "Invalid name, only alphabetical characters allowed."
    assert is_valid_name(
        "Basmala Rahma@") == "Invalid name, only alphabetical characters allowed."
    assert is_valid_name(
        "Basmala Rahma123") == "Invalid name, only alphabetical characters allowed."
    assert is_valid_name(
        "Basmala 444!") == "Invalid name, only alphabetical characters allowed."
    assert is_valid_name(
        "Basmala Rahma#") == "Invalid name, only alphabetical characters allowed."
    assert is_valid_name(
        "Basmala Rahma$") == "Invalid name, only alphabetical characters allowed."
    assert is_valid_name(
        "Basmala Rahma%") == "Invalid name, only alphabetical characters allowed."

    # Valid names
    assert is_valid_name("Rahma Atia") == True
    assert is_valid_name("Basmala Moahamed") == True
    assert is_valid_name("Huda Amr") == True
    assert is_valid_name("Karim Ghazy") == True
    assert is_valid_name("Mohamed Ali") == True
    assert is_valid_name("Sara Omar") == True


def test_is_missing():
    # email, passwors and confirmed password are missing
    assert is_missing("", "", "") == False

    # password is missing
    assert is_missing("basmala@gmail.com", "", "basmala") == False
    assert is_missing("rahmatia@gmail.com", "", "rahmatia") == False
    assert is_missing("hudamr@gmail.com", "", "hudamr") == False
    assert is_missing("harrypoter@gmail.com", "", "harrypoter") == False
    assert is_missing("karimghazy@gmail.com", "", "karimghazy") == False

    # email is missing
    assert is_missing("", "basmala", "basmala") == False
    assert is_missing("", "rahmatia", "rahmatia") == False
    assert is_missing("", "hudamr", "hudamr") == False
    assert is_missing("", "harrypoter", "harrypoter") == False
    assert is_missing("", "karimghazy", "karimghazy") == False

    # confirmed password is missing
    assert is_missing("basmala@gmail.com", "basmala", "") == False
    assert is_missing("rahmatia@gmail.com", "rahmatia", "") == False
    assert is_missing("hudamr@gmail.com", "hudamr", "") == False
    assert is_missing("harrypoter@gmail.com", "harrypoter", "") == False
    assert is_missing("karimghazy@gmail.com", "karimghazy", "") == False

    # all inputs are valid
    assert is_missing("basmala@gmil.com", "Basmala+1", "Basmala+1") == True
    assert is_missing("rahmatia@gmail.com",
                         "#1Rahmatia", "#1Rahmatia") == True
    assert is_missing("hudamr@gmail.com", "@Hudamr23", "@Hudamr23") == True
    assert is_missing("harrypoter@gmail.com",
                         "Harrypoter!1", "Harrypoter!1") == True
    assert is_missing("karimghazy@gmail.com",
                         "karimGhazy#9", "karimGhazy#9") == True


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

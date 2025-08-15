from project import check_email, check_missing, check_password, Valid_name


def test_email():
    # no email ("Invalid email address")
    assert check_email("basmala.com") == None
    assert check_email("basmala@gmail") == None
    assert check_email("basmala@.com") == None
    assert check_email("helloworld") == None
    assert check_email("basmala@") == None
    assert check_email("basmala@com") == None
    assert check_email("basmala@gm.com") == None

    # valid emails
    assert check_email("basmala@gmail.com") == "basmala@gmail.com"
    assert check_email("rahmatia@gmail.com") == "rahmatia@gmail.com"
    assert check_email("hudamr@gmail.com") == "hudamr@gmail.com"
    assert check_email("harrypoter@gmail.com") == "harrypoter@gmail.com"
    assert check_email("karimghazy@gmail.com") == "karimghazy@gmail.com"
    assert check_email("saman@gmail.com") == "saman@gmail.com"


def valid_name():

    # name should not be empty
    assert Valid_name("") == "Name: "

    #name should have first and last name
    assert Valid_name("basmala") == "Format: First_Name Last_Name."
    assert Valid_name("basmalarahma") == "Format: First_Name Last_Name."
    assert Valid_name("CS50") == "Format: First_Name Last_Name."
    assert Valid_name("Basmala Rahma 123") == "Format: First_Name Last_Name."
    assert Valid_name("BasmalaRahma@") == "Format: First_Name Last_Name."
    assert Valid_name("a b c d e") == "Format: First_Name Last_Name."

    #name should have only alphabetical characters
    assert Valid_name("#Basmala Rahma") == "Invalid name, only alphabetical characters allowed."
    assert Valid_name("Basmala Rahma@") == "Invalid name, only alphabetical characters allowed."
    assert Valid_name("Basmala Rahma123") == "Invalid name, only alphabetical characters allowed."
    assert Valid_name("Basmala 444!") == "Invalid name, only alphabetical characters allowed."
    assert Valid_name("Basmala Rahma#") == "Invalid name, only alphabetical characters allowed."
    assert Valid_name("Basmala Rahma$") == "Invalid name, only alphabetical characters allowed."
    assert Valid_name("Basmala Rahma%") == "Invalid name, only alphabetical characters allowed."
    
    #Valid names
    assert Valid_name("Rahma Atia") == True
    assert Valid_name("Basmala Moahamed") == True
    assert Valid_name("Huda Amr") == True
    assert Valid_name("Karim Ghazy") == True
    assert Valid_name("Mohamed Ali") == True
    assert Valid_name("Sara Omar") == True
    


def test_missing():
    # email, and password are missing
    assert check_missing("", "", "") == False

    # username is missing
    assert check_missing("basmala@gmail.com", "", "basmala") == False

    # email is missing
    assert check_missing("", "basmala", "basmala") == False
    
    # password is missing
    assert check_missing("basmala@gmail.com", "basmala", "") == False
    

    assert check_missing("basmala@gmil.com", "basmala", "basmala") == True


def test_password():
    # repeat password doesn't match
    assert check_password("Basmala", "Rahma") == False
    assert check_password("Basmala_123", "Rahma_456") == False
    assert check_password("Huda_789", "Karim_101") == False
    assert check_password("Mohamed@112", "Ali#123") == False
    assert check_password("Sara$456", "#Omar%789") == False
    assert check_password("Basmala", "Basmala_123") == False
    assert check_password("Rahma", "Rahma_456") == False
    assert check_password("Huda", "Huda_789") == False

    # repeat password matches
    assert check_password("Basmala_123", "Basmala_123") == True
    assert check_password("Rahma_456", "Rahma_456") == True
    assert check_password("Huda_789", "Huda_789") == True
    assert check_password("Karim_101", "Karim_101") == True
    assert check_password("Mohamed@112", "Mohamed@112") == True
    assert check_password("Ali#123", "Ali#123") == True 
    assert check_password("Sara$456", "Sara$456") == True
    assert check_password("#Omar%789", "#Omar%789") == True


from project import check_email, check_missing, check_name, check_password


def test_email():
    # no email ("Invalid email address")
    # capture = capsys.readouterr()
    assert check_email("basmala.com") == None
    assert check_email("basmala@gmail") == None
    assert check_email("basmala@gmail.com") == "basmala@gmail.com"


def test_name():
    assert check_name("") == "User"
    assert check_name("basmala") == "basmala"
    assert check_name("Karim") == "Karim"


def test_missing():
    assert check_missing("", "", "") == False
    assert check_missing("basmala@gmil.com", "basmala", "basmala") == True


def test_password():
    check_password("basmala", "rahma") == False
    check_password("basmala", "basmala") == True

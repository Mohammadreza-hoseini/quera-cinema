import pytest
from app.users import Users
#from .test_db_connection import cnx


def test_validate_user_name():

    assert Users.validate_user_name("") == -1
    assert Users.validate_user_name(None) == -1
    assert Users.validate_user_name("gholi") == -2
    assert Users.validate_user_name("gholi25") == -2
    assert Users.validate_user_name("Gholi")
    assert Users.validate_user_name("Gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25") == -2    
    assert Users.validate_user_name("Gholi522") == True


def test_validate_email():
    assert Users.validate_email("") == -1
    assert Users.validate_email(None) == -1
    assert Users.validate_email("gholigmail.com") == -2
    assert Users.validate_email("gholi@gmail.c") == -2
    assert Users.validate_email("gholi@gmail.com") == True


def test_alidate_phone_number():
    assert Users.validate_phone_number(None) == True
    assert Users.validate_phone_number("989121121212") == -1
    assert Users.validate_phone_number("+989121121212") == -1
    assert Users.validate_phone_number("9121121212") == -1
    assert Users.validate_phone_number("9121121212") == -1
    assert Users.validate_phone_number("091211212") == -1
    assert Users.validate_phone_number("09121121212") == True


def test_validate_password():
    Users.validate_password("") == -1
    Users.validate_password(None) == -1
    Users.validate_password("gholi") == -2
    Users.validate_password("Gholi") == -2
    Users.validate_password("Gholi2") == -2
    Users.validate_password("Gholi2$") == -2
    Users.validate_password("Gholi1425") == -2
    Users.validate_password("Gholi1425") == -2
    Users.validate_password("Gholi1425#") == -2
    Users.validate_password("@Ghol5#") == -2
    Users.validate_password("@Gholi5#") == True


@pytest.mark.parametrize(
        ("user_name","validate_user_name"),
        [
            ("",-1),
            (None,-1),
            ("ghol",-2),
            ("Gholi555",True),
            ("Gholi555",-3),
        ]
)
def test_register_user_name(user_name,validate_user_name):
    Users.register.user_name = user_name
    assert validate_user_name == validate_user_name


@pytest.mark.parametrize(
        ("user_email","validate_email"),
        [
            ("",-1),
            (None,-1),
            ("gholyahoo.com",-2),
            ("Gholi555@gmail.com",True),
            ("Gholi555@gmail.com",-3),
        ]
)
def test_register_email(user_email,validate_email):
    Users.register.user_email = user_email
    assert validate_email == validate_email


@pytest.mark.parametrize(
        ("new_password","confirm_password","validate_password","confirm_password_validation","confirm_password_is_vlid"),
        [
            ("Gholi1425","Gholi1425",-2,-2,True),
            ("@Gholi5#","@Gholi6#",True,True,False),
            ("@Gholi6#","@Gholi6#",True,True,True),



        ]
)
def test_change_password(new_password,confirm_password,validate_password,confirm_password_validation,confirm_password_is_vlid):
    Users.change_password.new_password = new_password
    Users.change_password.confirm_password = confirm_password
    assert validate_password == validate_password
    assert confirm_password_validation == confirm_password_validation
    assert confirm_password_is_vlid == confirm_password_is_vlid


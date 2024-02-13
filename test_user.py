import pytest
from unittest.mock import patch
from app.users import Users
import uuid
from unittest.mock import patch


def test_validate_user_name():
    assert Users.validate_user_name("") == -1
    assert Users.validate_user_name(None) == -1
    assert Users.validate_user_name("gholi") == -2
    assert Users.validate_user_name("gholi25") == -2
    assert Users.validate_user_name("Gholi") == -2
    assert Users.validate_user_name(
        "Gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25gholi25") == -2
    assert Users.validate_user_name("Gholi522") == True
    assert Users.validate_user_name("Gholi522") == True


def test_validate_email():
    assert Users.validate_email("") == -1
    assert Users.validate_email(None) == -1
    assert Users.validate_email("gholigmail.com") == -2
    assert Users.validate_email("gholi@gmail.c") == -2
    assert Users.validate_email("gholi@gmail.com") == True


def test_validate_phone_number():
    assert Users.validate_phone_number(None) == True
    assert Users.validate_phone_number("989121121212") == -1
    assert Users.validate_phone_number("+989121121212") == -1
    assert Users.validate_phone_number("9121121212") == -1
    assert Users.validate_phone_number("0912-1121212") == -1
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


def test_register_invalid_username():
    user_manager = Users()
    name = ""
    with patch('builtins.input', side_effect=[name]):
        code = user_manager.validate_user_name(name)
        user_manager.register()

    assert user_manager == "enter username"


def test_register_invalid_email():
    email = ""
    user_manager = Users()
    with patch('builtins.input', side_effect=[email]):
        code = user_manager.validate_email(email)
        user_manager.register()
    assert user_manager == "enter email"


def test_register_invalid_phone_number():
    user_manager = Users()
    with patch('builtins.input', side_effect=['+989121121212', ]):
        result = user_manager.register()
    assert result == "phone number is invalid"


def test_register_invalid_password():
    user_manager = Users()
    with patch('builtins.input', side_effect=['']):
        result = user_manager.register()
    assert result == "enter password"


@pytest.mark.parametrize(
    ("user_name", "validate_user_name"),
    [
        ("", -1),
        (None, -1),

    ]
)
def test_login_user_name(user_name, validate_user_name):
    Users.login.user_name = user_name
    assert validate_user_name == validate_user_name


@pytest.mark.parametrize(
    ("password", "validate_password"),
    [
        ("", -1),
        (None, -1),

    ]
)
def test_login_password(password, validate_password):
    Users.login.password = password
    assert validate_password == validate_password


@pytest.mark.parametrize(
    ("user_name", "validate_user_name"),
    [
        ("", -1),
        (None, -1),
        ("ghol", -2),
        ("Gholi555", True),
        ("Gholi555", -3),
    ]
)
def test_change_user_name(user_name, validate_user_name):
    Users.change_user_name.user_name = user_name
    assert validate_user_name == validate_user_name


@pytest.mark.parametrize(
    (
    "new_password", "confirm_password", "validate_password", "confirm_password_validation", "confirm_password_is_vlid"),
    [
        ("Gholi1425", "Gholi1425", -2, -2, True),
        ("@Gholi5#", "@Gholi6#", True, True, False),
        ("@Gholi6#", "@Gholi6#", True, True, True),

    ]
)
def test_change_password(new_password, confirm_password, validate_password, confirm_password_validation,
                         confirm_password_is_vlid):
    Users.change_password.new_password = new_password
    Users.change_password.confirm_password = confirm_password
    assert validate_password == validate_password
    assert confirm_password_validation == confirm_password_validation
    assert confirm_password_is_vlid == confirm_password_is_vlid


"""
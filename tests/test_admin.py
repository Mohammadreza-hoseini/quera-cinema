








"""import pytest
from app.admin import Admin


@pytest.mark.parametrize(
        ("validate_username_dict","username","user_validation"),
        [
            (-1,"",-1),
            (-1,None,-1),
            (-2,"ghol",-2),

        ]
)
def test_register(validate_username_dict,username,user_validation):
    admin_manager = Admin()
    admin_manager.register.username = username
    assert admin_manager.register.validate_username_dict == validate_username_dict
    assert admin_manager.register.user_validation == user_validation


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
def test_register_admin_email(user_email,validate_email):
    Admin.register.user_email = user_email
    assert validate_email == validate_email

@pytest.mark.parametrize(
        ("phone_number","validate_phone_number"),
        [
            ("",True),
            ("989121121212",-1),
            ("091211212",-1),
            ("09121121212",True),
        ]
)
def test_register_admin_phone_number(phone_number,validate_phone_number):
    Admin.register.phone_number = phone_number
    assert validate_phone_number == validate_phone_number


@pytest.mark.parametrize(
        ("password","validate_password"),
        [
            ("",-1),
            (None,-1),
            ("Gholi1425#",-2),
            ("@Gholi5#",True),
        ]
)
def test_register_admin_password(password,validate_password):
    Admin.register.password = password
    assert validate_password == validate_password
"""
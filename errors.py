class CustomError(Exception):
    def __init__(self, error_message):
        Exception.__init__(self)
        self.error_message = error_message

    def __str__(self):
        return self.error_message


class UnknownError(CustomError):
    def __init__(self):
        CustomError.__init__(self, 'Internal server error')


class InvalidArguments(CustomError):
    def __init__(self):
        CustomError.__init__(self, 'Invalid arguments')


class InvalidUsernameOrPassword(CustomError):
    def __init__(self):
        CustomError.__init__(self, 'Username or Password is wrong')


class InvalidEmail(CustomError):
    def __init__(self):
        CustomError.__init__(self, 'Email is invalid')


class InvalidPassword(CustomError):
    def __init__(self):
        CustomError.__init__(self, 'Password is invalid')


class InvalidUsername(CustomError):
    def __init__(self):
        CustomError.__init__(self, 'Username is invalid')


class ChangePassword(CustomError):
    def __init__(self):
        CustomError.__init__(self, 'Password not match')


class UsernameExist(CustomError):
    def __init__(self):
        CustomError.__init__(self, 'Username exist')


class EmailExist(CustomError):
    def __init__(self):
        CustomError.__init__(self, 'Email exist')


class InvalidPhoneNumber(CustomError):
    def __init__(self):
        CustomError.__init__(self, 'phone number is invalid')


class MovieNameDoesNotExist(CustomError):
    def __init__(self):
        CustomError.__init__(self, 'movie name does not exist')


class InvalidDate(CustomError):
    def __init__(self):
        CustomError.__init__(self, 'birth date is invalid')
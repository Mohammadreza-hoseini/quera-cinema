# TODO: bank_account, wallet, cinema, sit class
import uuid


# from {} import User


class BankAccount:
    # NOTE: User?
    def __init__(self, user: User, amount: int, cvv2: int, password: string):
        self.uuid = uuid.uuid4()

        self.user = user

        self.amount = amount

        # should be hashed?
        self.cvv2 = cvv2

        # should be hashed
        self.password = password

    # TODO
    def __str__(self):
        pass


class Wallet:
    # NOTE: User?
    def __init__(self, user: User, amount: int):
        self.uuid = uuid.uuid4()

        self.user = user

        self.amount = amount

    # TODO
    def __str__(self):
        pass


class Theater:
    def __init__(self, capacity: int, average_rate: float = -1):
        self.uuid = uuid.uuid4()

        self.capacity = capacity

        self.average_rate = average_rate

    # TODO
    def __str__(self):
        pass


class Sit:
    # NOTE: Theater?
    def __init__(self, theater: Theater, status: int = 0):
        self.uuid = uuid.uuid4()

        self.theater = theater

        if status in [0, 1]:
            self.status = status
        else:
            raise ValueError("status can be either 0 or 1")

    # TODO
    def __str__(self):
        pass

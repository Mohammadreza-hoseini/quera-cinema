import uuid
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

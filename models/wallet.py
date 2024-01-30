import uuid
class Wallet:
    # NOTE: User?
    def __init__(self, user: User, amount: int):
        self.uuid = uuid.uuid4()

        self.user = user

        self.amount = amount

    # TODO
    def __str__(self):
        pass

import uuid
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
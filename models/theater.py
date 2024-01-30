import uuid
class Theater:
    def __init__(self, capacity: int, average_rate: float = -1):
        self.uuid = uuid.uuid4()

        self.capacity = capacity

        self.average_rate = average_rate

    # TODO
    def __str__(self):
        pass

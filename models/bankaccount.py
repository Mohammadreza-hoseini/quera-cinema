# CREATE TABLE `BankAccount` (
#   `id` char(36) PRIMARY KEY,
#   `user_id` CHAR(36) NOT NULL,
#   `amount` int NOT NULL,
#   `cvv2` int NOT NULL ,
#   `created_at` timestamp default current_timestamp
#   `password` varchar(255) NOT NULL
# );

#   //deposit(variz) | withdrawal(bardaasht) | transfer(enteghal)
#   // withdrawal: user subscription should be considered
#   // constraints: withdrawal <= amount && transfer <= amount

import hashlib
import re


from connection import connection


class BankAccount:
    def __init__(self):
        pass

    # transaction table? #TODO
    def commit_transaction(
        self, user_id: str, transaction_type: int, transaction_amount: float
    ):
        """
        transaction_type:  1: withdrawal | 2: transfer | 3: deposit
        """

        if transaction_type in [1, 2]:
            valid = self.validate_transaction(transaction_amount)
            if valid:
                # check user subscription #TODO:
                discount = 0
                self.amount -= (100 - discount) / 100 * transaction_amount

                # transfer destination account #TODO:

                # Database log #TODO: LOG
            else:
                self.amount += transaction_amount
                # TODO: LOG
                # raise Exception
                pass

    def validate_transaction(self, transaction_amount: float) -> bool:
        """
        Check transaction for withdrawal and transfer
        """
        return self.amount >= transaction_amount

    @staticmethod
    def validate_credential(credential: str) -> bool:
        if credential == "" or credential is None:
            print("enter password")
        pattern = r"^(?=.*[a-zA-Z].*[a-zA-Z])(?=.*[@#$&]).{8,}$"
        if not re.match(pattern, credential):
            return False
        hashed_credential = hashlib.sha256(credential.encode()).hexdigest()
        return hashed_credential

    @classmethod
    def create_account(
        cls, user_id: str, initial_amount: float, cvv2: int, password: str
    ):
        # check user_id #TODO

        # check password, cvv2 format #TODO

        # uuid #TODO
        if valid:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO BankAccount(id, user_id, amount, cvv2, created_at, password)
                VALUES ( uuid(), %s, %s, %s, current_timestamp, %s)""",
                (user_id, initial_amount, cvv2, self.validate_credential(password)),
            )
            # cls( , user_id, initial_amount, cvv2, password)

        pass

    def __str__(self):
        pass

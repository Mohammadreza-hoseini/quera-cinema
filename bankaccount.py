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
from typing import Union

from connection import connection


class BankAccount:
    def __init__(self):
        pass

    # should BankAccount table have separate password  #QUESTION:
    def login(self):
        pass

    def __charge_wallet(self, transaction_amount):
        self.amount -= transaction_amount
        # charge wallet#TODO:
        pass

    def __withdrawal(self, transaction_amount):
        # check user subscription #TODO:
        discount = 0

        self.amount -= transaction_amount
        # log #LOG

    def __deposit(self, transaction_amount):
        self.amount += transaction_amount

    def __transfer(self, transaction_amount):
        final_bank_account_id = input(
            "Enter bank_account_id you want to transfer into: "
        )
        # check if bank_account_id exists #TODO
        # add amount to final_bank_account

        self.amount -= transaction_amount

    # transaction table? #TODO
    def commit_transaction(
        self, user_id: str, transaction_type: int, transaction_amount: float
    ) -> None:
        """
        transaction_type:  1: withdrawal | 2: transfer to another account | 3: charge wallet | 4: deposit
        """

        if transaction_type in [1, 2, 3]:
            valid = self.validate_transaction(transaction_amount)
            if valid:
                transaction_func_dict = {
                    1: self.__withdrawal,
                    2: self.__transfer,
                    3: self.__charge_wallet,
                }
                transaction_func_dict[transaction_type](transaction_amount)
                # Database log #TODO: LOG
            else:
                self.__deposit(transaction_amount)

    # DONE
    def validate_transaction(self, transaction_amount: float) -> bool:
        """
        Check transaction for withdrawal, transfer and wallet charge
        """
        return self.amount >= transaction_amount

    # DONE
    @staticmethod
    def validate_credential(credential: str) -> Union[bool, str]:
        """_summary_
                validate bank_account password format for creating account

        Returns:
            Union[bool, str]:
                bool -> returns False (if the format is wrong)
                str -> returns hashed password
        """
        if credential == "" or credential is None:
            return False
        pattern = r"^(?=.*[a-zA-Z].*[a-zA-Z])(?=.*[@#$&]).{8,}$"
        if not re.match(pattern, credential):
            return False

        hashed_credential = hashlib.sha256(credential.encode()).hexdigest()
        return hashed_credential

        # User table query check credential #TODO
        # return True | False

    # DONE
    @classmethod
    def create_account(
        cls, user_id: str, initial_amount: float, cvv2: int, password: str
    ) -> None:
        # check user_id #TODO

        # check password, cvv2 format #TODO

        # uuid #TODO
        if valid:
            cursor = connection.cursor()
            hashed_pass = self.validate_credential(password)
            cursor.execute(
                """
                INSERT INTO BankAccount(id, user_id, amount, cvv2, created_at, password)
                VALUES ( uuid(), %s, %s, %s, current_timestamp, %s)""",
                (user_id, initial_amount, cvv2, hashed_pass),
            )
            # cls( , user_id, initial_amount, cvv2, password)

        pass

    def __str__(self):
        pass


############## test:

new_bank_acccount = BankAccount.create_account("123231", 102.5, 342, "aA1#@fjskldfsjlk")

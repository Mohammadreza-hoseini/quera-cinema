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
import random
import re
from typing import Union

from connection import connection
from BA_login_decorator import user_login_decorator, BA_login_decorator

cursor = connection.cursor()


class BankAccount:
    def __init__(self):
        pass

    # def login(self):
    #     pass

    @staticmethod
    def bank_account_balance(card_number: int) -> float:
        """_summary_
        returns current amount of money in specified card_number
        """
        cursor.execute(
            f"SELECT amount FROM BankAccount WHERE card_number = {card_number}"
        )

        current_amount = float(cursor.fetchone()[0])
        return current_amount

    @staticmethod
    @user_login_decorator  # login #TODO
    def __charge_wallet(
        cls, user_id: str, card_number: int, transaction_amount: float
    ) -> None:
        """_summary_
        Charge wallet with card_number
        """

        current_amount = cls.bank_account_balance(card_number)
        updated_amount = current_amount - transaction_amount
        cursor.execute(
            f"UPDATE BankAccount SET amount = {updated_amount} WHERE card_number = {card_number}"
        )

        # get current_wallet_amount #TODO
        # updated_wallet_amount = transaction_amount + current_wallet_amount
        # #BUG
        cursor.execute(
            f"UPDATE Wallet SET amount = {transaction_amount} WHERE user_id = {user_id}"
        )
        connection.commit()

    @classmethod
    @user_login_decorator  # for user login #TODO
    def __withdrawal(cls, card_number: int, transaction_amount: float) -> None:
        """_summary_
        Subtract money from account based on user subscription
        """
        # check user subscription #TODO:
        discount = 0

        self.amount -= transaction_amount
        # log #LOG

    @classmethod
    def __deposit(cls, card_number: int, transaction_amount: float) -> float:
        """_summary_
        add money to account
        """
        current_amount = cls.bank_account_balance(card_number)
        updated_amount = current_amount + transaction_amount
        cursor.execute(
            f"UPDATE BankAccount SET amount = {updated_amount} WHERE card_number = {card_number}"
        )
        connection.commit()

    @classmethod
    def __transfer(
        cls, card_number: int, transaction_amount: float, card_number2: int
    ) -> None:
        """_summary_
        Transfer money from one account to another account
        """

        # check if bank_account_id exists #TODO
        # add amount to final_bank_account

        # subtract from card_number1
        current_amount_account1 = cls.bank_account_balance(card_number)
        updated_amount_account1 = current_amount_account1 - transaction_amount
        cursor.execute(
            f"UPDATE BankAccount SET amount = {updated_amount_account1} WHERE card_number = {card_number}"
        )

        # add to card_number2
        current_amount_account2 = cls.bank_account_balance(card_number2)
        updated_amount_account2 = current_amount_account2 + transaction_amount
        cursor.execute(
            f"UPDATE BankAccount SET amount = {updated_amount_account2} WHERE card_number = {card_number2}"
        )

        connection.commit()

    # transaction table? #TODO
    @classmethod
    @BA_login_decorator
    def commit_transaction(
        cls,
        user_id: str,
        card_number: int,
        transaction_type: int,
        transaction_amount: float,
        card_number2: int = -1,
    ) -> None:
        """_summary_
        transaction_type:  1: withdrawal | 2: transfer to another account | 3: charge wallet | 4: deposit
        """

        if transaction_type in [1, 2, 3]:
            current_amount = cls.bank_account_balance(card_number)
            valid = current_amount >= transaction_amount
            if valid:
                if transaction_type == 1:
                    cls.__withdrawal(card_number, transaction_amount)
                if transaction_type == 2:
                    if card_number2 == -1:
                        print("Second_card_number not giver\n")
                    else:
                        print("JJJJJJJJJ")
                        print(card_number, transaction_amount, card_number2)
                        cls.__transfer(card_number, transaction_amount, card_number2)
                if transaction_type == 3:
                    cls.__charge_wallet(user_id, card_number, transaction_amount)
                print("Successful transactrion\n")
                # Database log #TODO: LOG
            else:
                print("Invalid transaction\n")
        else:
            cls.__deposit(card_number, transaction_amount)
            print("Successful transactrion\n")

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
        """
        Create bank account
        """
        # check user_id #TODO

        # check password, cvv2 format #TODO

        # uuid #TODO
        valid = 1  # should be changed
        if valid:
            hashed_pass = cls.validate_credential(password)
            card_number = random.randint(int(1e15), int(1e16))  # possible #BUG?
            cursor.execute(
                """
                INSERT INTO BankAccount
                VALUES ( uuid(), %s, %s, %s, current_timestamp, %s, %s)""",
                (user_id, initial_amount, cvv2, hashed_pass, card_number),
            )  # initial amount is not stored as float #BUG:
            connection.commit()
            print(f"Bank_account created\n")

        else:
            print("Invalid input\n")

    def __str__(self):
        pass


############## test:
bk1 = BankAccount()

# new_bank_acccount = bk1.create_account(
#     "c599b937-c273-11ee-9027-0242ac150202", 33, 342, "abbasali@34"
# )

# bk1.commit_transaction(
#     user_id="c599b937-c273-11ee-9027-0242ac150202",
#     card_number=7557812553883616,
#     transaction_type=4,
#     transaction_amount=100,
# )


bk1.commit_transaction(
    user_id="c599b937-c273-11ee-9027-0242ac150202",
    card_number=7557812553883616,
    transaction_type=2,
    transaction_amount=10,
    card_number2=7939441481282623,
)

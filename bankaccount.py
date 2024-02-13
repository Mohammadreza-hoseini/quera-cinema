import hashlib
import os
import random
import re
from typing import Union

from connection import connection

cursor = connection.cursor()


class BankAccount:
    def __init__(self):
        pass

    @staticmethod
    def get_user_accounts(user_id: str):
        cursor.execute(
            f"""SELECT id, card_number FROM BankAccount WHERE user_id= {user_id.__repr__()}"""
        )
        user_accounts = cursor.fetchall()
        if not user_accounts:
            return -1  # User doesn't have account
        return user_accounts

    @classmethod
    def login(cls, user_id: str):
        print("#### Login Bank Account ####")

        user_bank_accounts = cls.get_user_accounts(user_id)
        # print(user_bank_accounts)

        if user_bank_accounts == -1:
            print("User doesn't have account: ")
            return

        card_number = input("Enter card number: ")

        while not card_number.isdigit():
            os.system("cls")
            print("Invalid card_number")
            card_number = input("Enter card number: ")

        account_id = -1
        card_number = int(card_number)
        while account_id == -1:
            for valid_account_id, valid_card_number in user_bank_accounts:
                if valid_card_number == card_number:
                    account_id = valid_account_id
                    break
            if account_id == -1:
                os.system("cls")
                print("Invalid card number")
                card_number = input("Enter card number: ")

        password = input("Enter your bank password: ")

        cursor.execute(
            f"""SELECT password, cvv2 FROM BankAccount WHERE user_id= {user_id.__repr__()} AND id={account_id.__repr__()}"""
        )
        data = cursor.fetchone()

        correct_hashed_pass = data[0]
        password_validation = cls.validate_credential(password)

        while password_validation != correct_hashed_pass:
            os.system("cls")
            print("Password is invalid")
            password = input("Enter your bank password: ")
            password_validation = cls.validate_credential(password)

        correct_cvv2 = data[1]
        cvv2 = input("Enter your bank cvv2: ")

        while not cvv2.isdigit() or int(cvv2) != correct_cvv2:
            os.system("cls")
            print("Invalid cvv2")
            cvv2 = input("Enter your bank cvv2: ")

        cursor.execute(
            f"""UPDATE BankAccount SET logged_in ={1} WHERE id={account_id.__repr__()}"""
        )
        connection.commit()
        print("Logged in")

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
    def __charge_wallet(
        user_id: str, card_number: int, transaction_amount: float
    ) -> None:
        """_summary_
        Charge wallet with card_number
        """

        current_amount = BankAccount.bank_account_balance(card_number)
        updated_amount = current_amount - transaction_amount
        cursor.execute(
            f"UPDATE BankAccount SET amount = {updated_amount} WHERE card_number = {card_number}"
        )

        cursor.execute(
            f"SELECT amount FROM Wallet WHERE user_id = {user_id.__repr__()}"
        )
        current_wallet_amount = cursor.fetchone()[0]

        new_wallet_amount = current_wallet_amount + transaction_amount
        cursor.execute(
            f"UPDATE Wallet SET amount = {new_wallet_amount} WHERE user_id = {user_id.__repr__()}"
        )
        connection.commit()

    @classmethod
    def __withdrawal(cls, card_number: int, transaction_amount: float) -> None:
        """_summary_
        Subtract money from account based on user subscription
        """
        current_amount = cls.bank_account_balance(card_number)
        updated_amount = current_amount - transaction_amount
        cursor.execute(
            f"""UPDATE BankAccount SET amount={updated_amount} WHERE card_number = {card_number}"""
        )
        connection.commit()

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
    def commit_transaction(
        cls,
        user_id: str,
        card_number: int,
        transaction_amount: float,
        card_number2: int = -1,
    ) -> None:
        """_summary_
        transaction_type:  1: withdrawal | 2: transfer to another account | 3: charge wallet | 4: deposit
        """
        print(
            f"""####Allowed operations####
              1: withdrawal
              2: transfer
              3: charge_wallet
              4: deposit"""
        )

        ALLOWED_OPERATIONS = {
            1: "withdrawal",
            2: "transfer",
            3: "charge_wallet",
            4: "deposit",
        }

        transaction_type = input("Operation: ")
        while (not transaction_type.isdigit()) or (
            int(transaction_type) not in ALLOWED_OPERATIONS
        ):
            os.system("cls")
            print("Invalid operation")
            print(
                f"""####Allowed operations####
              1: withdrawal
              2: transfer
              3: charge_wallet
              4: deposit"""
            )
            transaction_type = input("Operation: ")
        transaction_type = int(transaction_type)

        if transaction_type in [1, 2, 3]:
            current_amount = cls.bank_account_balance(card_number)
            valid = current_amount >= transaction_amount
            if valid:
                if transaction_type == 1:
                    cls.__withdrawal(card_number, transaction_amount)
                if transaction_type == 2:
                    if card_number2 == -1:
                        print("Second_card_number not given\n")
                    else:
                        cls.__transfer(card_number, transaction_amount, card_number2)
                if transaction_type == 3:
                    cls.__charge_wallet(user_id, card_number, transaction_amount)
                print("Successful transactrion\n")
                # Database log #TODO: LOG
            else:
                print("Not enough money\n")
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
            return -1
        pattern = r"^(?=.*[a-zA-Z].*[a-zA-Z])(?=.*[@#$&]).{8,}$"
        if not re.match(pattern, credential):
            return -1

        hashed_credential = hashlib.sha256(credential.encode()).hexdigest()
        return hashed_credential

        # User table query check credential #TODO
        # return True | False

    # DONE
    @classmethod
    def create_account(cls, user_id: str, initial_amount: float) -> None:
        """
        Create bank account
        """
        print("#### Create Bank Account ####")

        password = input("Enter your bank password: ")
        validate_password = {-1: "Password is invalid"}
        password_validation = cls.validate_credential(password)
        while password_validation in validate_password:
            os.system("cls")
            print(validate_password[password_validation])
            password = input("Enter your bank password: ")
            password_validation = cls.validate_credential(password)

        hashed_pass = password_validation  # it returns the hashed_pass

        cvv2 = random.randint(int(1e4), int(1e5))  # possible #BUG?

        card_number = random.randint(int(1e15), int(1e16))  # possible #BUG?
        cursor.execute(
            f"""
            INSERT INTO BankAccount
            VALUES ( uuid(), {user_id.__repr__()}, {initial_amount},  {cvv2}, current_timestamp, {hashed_pass.__repr__()}, {card_number}, {0})""",
        )
        connection.commit()
        print(f"Bank_account created\n")

    def __str__(self):
        pass


if __name__ == "__main__":
    ############## test:
    bk1 = BankAccount()

    # new_bank_acccount = bk1.create_account(
    #     "c61e4977-aeaa-4721-a72d-bff5a83a47d5", 78.59
    # )

    bk1.commit_transaction(
        user_id="a75d1ce3-78dc-4e60-be8c-5b90c00b09cb",
        card_number=6538612319900380,
        transaction_amount=2,
        card_number2=6859275337830227,
    )

    # bk1.login("a75d1ce3-78dc-4e60-be8c-5b90c00b09cb")

    # bk1.commit_transaction(
    #     user_id="c599b937-c273-11ee-9027-0242ac150202",
    #     card_number=7557812553883616,
    #     transaction_type=4,
    #     transaction_amount=100,
    # )

    # bk1.commit_transaction(
    #     user_id="c599b937-c273-11ee-9027-0242ac150202",
    #     card_number=7557812553883616,
    #     transaction_type=2,
    #     transaction_amount=10,
    #     card_number2=7939441481282623,
    # )
# ght23@jsE

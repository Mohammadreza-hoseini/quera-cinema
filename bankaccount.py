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

        if user_bank_accounts == -1:
            print("User doesn't have account: ")
            return -2

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
                while not card_number.isdigit():
                    os.system("cls")
                    print("Invalid card_number")
                    card_number = input("Enter card number: ")
                card_number = int(card_number)
            else:
                break

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
        return card_number

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
    def charge_wallet(
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
        current_wallet_amount = float(cursor.fetchone()[0])

        new_wallet_amount = current_wallet_amount + transaction_amount
        cursor.execute(
            f"UPDATE Wallet SET amount = {new_wallet_amount} WHERE user_id = {user_id.__repr__()}"
        )
        connection.commit()
        print("wallet charged")

    @classmethod
    def withdrawal(cls, card_number: int, transaction_amount: float) -> None:
        """_summary_
        Subtract money from account based on user subscription
        """
        current_amount = cls.bank_account_balance(card_number)
        updated_amount = current_amount - transaction_amount
        cursor.execute(
            f"""UPDATE BankAccount SET amount={updated_amount} WHERE card_number = {card_number}"""
        )
        connection.commit()
        print("withdrawal Done")

    @classmethod
    def deposit(cls, card_number: int, transaction_amount: float) -> float:
        """_summary_
        add money to account
        """
        current_amount = cls.bank_account_balance(card_number)
        updated_amount = current_amount + transaction_amount
        cursor.execute(
            f"UPDATE BankAccount SET amount = {updated_amount} WHERE card_number = {card_number}"
        )
        connection.commit()
        print("deposit Done")

    @classmethod
    def transfer(cls, card_number: int, transaction_amount: float) -> None:
        """_summary_
        Transfer money from one account to another account
        """
        card_number2 = input("Second card_number: ")

        while not card_number2.isdigit():
            os.system("cls")
            print("Invalid card_number")
            card_number2 = input("Second card_number: ")
        card_number2 = int(card_number2)
        cursor.execute(
            f"""SELECT 1 FROM BankAccount WHERE card_number={card_number2}"""
        )
        data = cursor.fetchone()
        while data is None:
            print("Second card_number is invalid")
            card_number2 = input("Second card_number: ")
            while not card_number2.isdigit():
                os.system("cls")
                print("Invalid card_number")
                card_number2 = input("Second card_number: ")
            card_number2 = int(card_number2)
            cursor.execute(
                f"""SELECT 1 FROM BankAccount WHERE card_number={card_number2}"""
            )
            data = cursor.fetchone()

        if card_number == card_number2:
            print("You've entered the same card_number")
            return

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
        print("transfer Done")

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


def bank_menu():
    print(
        f"""####Allowed operations####
            -1: Logout
            1: withdrawal
            2: transfer
            3: charge_wallet
            4: deposit"""
    )

    ALLOWED_OPERATIONS = {
        -1: "Logout",
        1: "withdrawal",
        2: "transfer",
        3: "charge_wallet",
        4: "deposit",
    }

    transaction_type = input("Bank Operation: ")
    while (not transaction_type.isdigit() and transaction_type != "-1") or (
        int(transaction_type) not in ALLOWED_OPERATIONS
    ):
        os.system("cls")
        print("Invalid operation", transaction_type)
        print(
            f"""####Allowed operations####
            -1: Logout
            1: withdrawal
            2: transfer
            3: charge_wallet
            4: deposit"""
        )
        transaction_type = input("Bank Operation: ")
    transaction_type = int(transaction_type)

    if transaction_type == -1:  # logout from bank account
        return -1
    if transaction_type == 1:
        return BankAccount.withdrawal
    if transaction_type == 2:
        return BankAccount.transfer
    if transaction_type == 3:
        return BankAccount.charge_wallet
    if transaction_type == 4:
        return BankAccount.deposit


if __name__ == "__main__":
    ############## test:
    bk1 = BankAccount()

    # new_bank_acccount = bk1.create_account(
    #     "c61e4977-aeaa-4721-a72d-bff5a83a47d5", 78.59
    # )

    # bk1.login("a75d1ce3-78dc-4e60-be8c-5b90c00b09cb")

# ght23@jsE
# 6538612319900344

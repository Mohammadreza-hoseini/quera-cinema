from connection import connection

cursor = connection.cursor()


class Wallet:
    def __init__(self):
        pass

    @staticmethod
    def wallet_balance(user_id: str) -> float:
        """_summary_
        Returns current amount of money in user's wallet
        """

        cursor.execute(
            f"SELECT amount FROM Wallet WHERE user_id = {user_id.__repr__()}"
        )

        current_amount = float(cursor.fetchone()[0])
        return current_amount

    @staticmethod
    def create_wallet(user_id: str) -> None:
        """
        Create wallet for user
        """

        cursor.execute(
            "INSERT INTO Wallet VALUES(uuid(), %s, current_timestamp, %s)", (user_id, 0)
        )
        connection.commit()

        print("Wallet added")

    @classmethod
    def pay_from_wallet(cls, user_id: str, transaction_amount: float):
        """
        Pay ticket price from wallet
        """

        current_wallet_amount = cls.wallet_balance(user_id)
        if transaction_amount > current_wallet_amount:
            print("Not enough money")
        else:
            new_wallet_amount = current_wallet_amount - transaction_amount
            cursor.execute(
                f"""UPDATE Wallet SET amount = {new_wallet_amount} WHERE user_id={user_id.__repr__()}"""
            )
            print("Paid from wallet")
            connection.commit()

    def __str__(self):
        pass


if __name__ == "__main__":

    w1 = Wallet()
    # w1.create_wallet("3075600f-c29c-11ee-9027-0242ac150202")

    w1.pay_from_wallet("a75d1ce3-78dc-4e60-be8c-5b90c00b09cb", 3000000)

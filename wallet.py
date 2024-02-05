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


from connection import connection

cursor = connection.cursor()


class Wallet:
    def __init__(self):
        pass

    @staticmethod
    def wallet_balance(user_name: str) -> float:
        """_summary_
        returns current amount of money in specified user wallet
        """

        cursor.execute(f"SELECT id FROM User WHERE username = {user_name.__repr__()}")
        user_id = cursor.fetchone()[0]

        cursor.execute(
            f"SELECT amount FROM Wallet WHERE user_id = {user_id.__repr__()}"
        )

        current_amount = float(cursor.fetchone()[0])
        return current_amount

    @staticmethod
    def create_wallet(user_name: str) -> None:
        cursor.execute(f"SELECT id FROM User WHERE username = {user_name.__repr__()}")
        user_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO Wallet VALUES(uuid(), %s, current_timestamp, %s)", (user_id, 0)
        )
        connection.commit()

    def __str__(self):
        pass


# w1 = Wallet()
# w1.create_wallet("Arman123")

# print(w1.wallet_balance('Arman123'))


############## test:
# w1 = Wallet()

import threading
import users




def main(user_input):
    user_input = int(user_input)
    print(f"request_handler {user_input}")
    thread = threading.Thread(target=users.main, args=(user_input,))
    return thread


# if __name__ == "__main__":
#     main()

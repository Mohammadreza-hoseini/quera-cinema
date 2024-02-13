import socket

HOST = "127.0.0.1"
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        user_input = "initial_input"
        menu = """
        1: Register
        2: Login
        3: Logout
        """
        print(menu)
        while user_input not in ['1', '2', '3']:
            user_input = input()
        if user_input == '3':
            break
        s.sendall(user_input.encode())
        
            

    print(f"client: {data}")

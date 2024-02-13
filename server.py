import socket
import request_handler

HOST = "127.0.0.1"
PORT = 8000



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"connected by {addr}")
        while True:
            
            user_input = conn.recv(1024).decode()
            print(f"server {user_input}")
            
            thread = request_handler.main(user_input)
            thread.start()
            thread.join()
            
            
            
            # request_handler.main(user_input)
            if not user_input:
                break
            # conn.sendall(thread)

import socket
import pickle

def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "localhost"
    server_port = 8000
    client.connect((server_ip, server_port))

    try:
        while True:
            msg = input("Enter message: ")
            client.send(msg.encode("utf-8")[:1024])

            response = client.recv(1024)
            print("Salam")
            response = pickle.loads(response)
            
            response()

            if response.lower() == "closed":
                break

            print(f"Received: {response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection to server closed")


run_client()

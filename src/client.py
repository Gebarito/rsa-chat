import socket, threading
import rsa, server

SERVER_ADDRESS="127.0.0.1"
SERVER_PORT=12000
username=""

def start_client() -> socket.socket:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_ADDRESS, SERVER_PORT))
    return client

def send_message(client: socket.socket) -> None:
    while True:
        message = input("Digite a mensagem: ")
        if message == 'quit':
            break
        message = f"{username}: {message}"
        message = rsa.encrypt(message, server.public_key)
        client.send(message.encode('utf-8'))

def receive_message(client: socket.socket) -> None:
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'quit':
                break
            message = rsa.decrypt(message, server.private_key)
            print(message)
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    conn = start_client()
    username = input("Digite seu nome: ")

    while conn:
        threading.Thread(target=send_message, args=(conn,)).start()
        threading.Thread(target=receive_message, args=(conn,)).start()

    conn.close()

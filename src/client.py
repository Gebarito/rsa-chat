import socket
import threading
import pickle
from constants import SERVER_ADDRESS, SERVER_PORT, PUBLIC_KEY, PRIVATE_KEY
import rsa

username = ""

def start_client() -> socket.socket:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_ADDRESS, SERVER_PORT))
    return client

def send_message(client: socket.socket) -> None:
    while True:
        message = input("")
        if message == 'quit':
            client.send(b'quit')
            break
        plaintext = username + ": " + message
        encrypted_message = rsa.encrypt(plaintext, PUBLIC_KEY)
        client.send(pickle.dumps(encrypted_message))

def receive_message(client: socket.socket) -> None:
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break
            if data == b'quit':
                break
            encrypted_message = pickle.loads(data)
            decrypted_message = rsa.decrypt(encrypted_message, PRIVATE_KEY)
            print(f'\nMensagem recebida:{decrypted_message}\n')
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    conn = start_client()
    username = input("Digite seu nome: ")

    threading.Thread(target=send_message, args=(conn,), daemon=True).start()
    threading.Thread(target=receive_message, args=(conn,), daemon=True).start()

    while True:
        pass

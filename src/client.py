import socket, threading
import rsa
from constants import SERVER_ADDRESS, SERVER_PORT


keys = []
def start_client() -> socket.socket:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_ADDRESS, SERVER_PORT))
    except Exception as e:
        print(f"Erro ao conectar ao servidor: {e}")

    return client

def send_message(client: socket.socket) -> None:
    while True:
        msg = input('Digite sua mensagem: ')
        if msg == 'quit':
            exit()
        
        try:
            pub_key, priv_key = rsa.generate_keys()
            keys.append((msg, pub_key, priv_key)) # Armazena chaves para cada mensagem para descriptografia em outro client;
            encrypted_msg = rsa.encrypt(msg, pub_key)
            client.send(str(encrypted_msg).encode('utf-8'))
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            break

def receive_message(client: socket.socket) -> None:
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break

            decrypted_msg = rsa.decrypt(msg, keys[-1][2])
            print(f"Mensagem recebida: {decrypted_msg}")
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            break


if __name__ == "__main__":
    conn = start_client()

    while conn:
        threading.Thread(target=send_message, args=(conn,)).start()
        #threading.Thread(target=receive_message, args=(conn,)).start()

    conn.close()

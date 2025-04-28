import socket
import threading
from constants import SERVER_ADDRESS, SERVER_PORT

connections = []

def handle_client(client) -> None:
    '''
    Envia e recebe as mensagens dos clientes.
    '''
    while True:
        try:
            data = client.recv(4096)
            if not data:
                break
            if data == b'quit':
                break
            print(f"Recebido: {data}")
            for conn in connections:
                if conn != client:
                    conn.send(data)
        except Exception as e:
            print(f"Error: {e}")
            break
    client.close()
    connections.remove(client)

def run_server() -> None:
    '''
    Inicia o servidor.
    '''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((SERVER_ADDRESS, SERVER_PORT))
        server.listen()
    except Exception as e:
        return print(f"Erro ao iniciar servidor: {e}")

    print(f"Servidor rodando em {SERVER_ADDRESS}:{SERVER_PORT}")

    while True:
        client, addr = server.accept()
        connections.append(client)
        print(f"Conectado a {addr}")
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()

if __name__ == "__main__":
    run_server()

    for conn in connections:
        conn.close()
    print("Servidor encerrado.")

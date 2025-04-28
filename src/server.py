import socket, threading
from rsa import generate_keys

SERVER_ADDRESS="127.0.0.1"
SERVER_PORT=12000
connections = []
public_key, private_key = generate_keys()

def handle_client(client) -> None:
    '''
        Envia e recebe as mensagens dos clientes.

        param client: socket do cliente
        type client: socket.socket
        return: None
    '''
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == 'quit':
                break
            print(msg)
            for conn in connections:
                if conn != client:
                    conn.send(msg.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            break
    client.close()

def run_server() -> None:
    '''
        Inicia o servidor.

        return: None
    '''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('127.0.0.1', 12000))
        server.listen()
    except Exception as e:
        return print(f"Erro ao iniciar servidor: {e}")	
    
    while True:
        client, addr = server.accept()
        connections.append(client)
        print(f"Conectado a {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    run_server()

    for conn in connections:
        conn.close()
    print("Servidor encerrado.")

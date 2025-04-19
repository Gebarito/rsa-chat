# Executa um server e 2 clientes em terminais diferentes

gnome-terminal -- bash -c "python3 src/server.py; exec bash"
gnome-terminal -- bash -c "python3 src/client.py; exec bash"
gnome-terminal -- bash -c "python3 src/client.py; exec bash"

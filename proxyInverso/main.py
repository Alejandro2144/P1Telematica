import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    server_setup()
    run_server()
    server_socket.close()

def server_setup():
    server_socket.bind(("localhost", 8080))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.listen(3)
    print("Se estableció correctamente la conexión")

def handle_connection(socket_conection, direction):
    print(f'Conectado {direction[0]}:{direction[1]}')
    conectado = True
    data_recevived = socket_conection.recv(2048)
    print(data_recevived)
    print('Desconectado')
    socket_conection.close()


def run_server():
    while True:
        socket_conection, direction = server_socket.accept()
        client_thread = threading.Thread(target=handle_connection, args=(socket_conection,direction))
        client_thread.start()

if __name__ == "__main__":
    main()
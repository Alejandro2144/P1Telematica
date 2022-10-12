import socket
from sqlite3 import connect
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_IP = "54.211.10.255"
SERVER_PORT = 8080
HTTP_HEADER_DELIMITER = b'\r\n\r\n'
CONTENT_LENGTH_FIELD = 'Content-Length: '
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
    data_recevived = recv_message(socket_conection)
    # print(data_recevived)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(((SERVER_IP, SERVER_PORT)))
    #Reconocer 
    url = ('HEAD '+ data_recevived.decode().split('\r\n')[0].split()[1] + ' HTTP/1.1\r\nHost: '+SERVER_IP+':'+str(SERVER_PORT)+'\r\n\r\n').encode()
    client_socket.sendall(url)
    msg = recv_message(client_socket)
    head = msg.decode().split('\r\n')
    length = len(msg)
    for headers in head:
        if headers.startswith(CONTENT_LENGTH_FIELD):
            length = int(headers.split()[1])
    client_socket.sendall(data_recevived)
    data = recv_message_with_size(client_socket, length)
    socket_conection.sendall(data)
    print('Desconectado')
    socket_conection.close()

def recv_message(recv_socket):
    BUFF_SIZE = 8192
    packet = recv_socket.recv(BUFF_SIZE)
    return packet

def recv_message_with_size(recv_socket, size):
    BUFF_SIZE = 8192
    data = b''
    while size - len(data) > 0:
        packet = recv_socket.recv(BUFF_SIZE)
        data += packet
        print(data)
        print(size, len(data))
    return data


def get_API_data(client_socket):
    pass

def run_server():
    while True:
        socket_conection, direction = server_socket.accept()
        client_thread = threading.Thread(target=handle_connection, args=(socket_conection,direction))
        client_thread.start()

if __name__ == "__main__":
    main()
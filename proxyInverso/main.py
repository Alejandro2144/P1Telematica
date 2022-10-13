import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER_IP = "3.95.202.86"
SERVER_PORT = 8080
HTTP_HEADER_DELIMITER = b'\r\n\r\n'
CONTENT_LENGTH_FIELD = b'Content-Length: '
def main():
    server_setup()
    run_server()
    server_socket.close()

def server_setup():
    server_socket.bind(("localhost", 8080))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.listen(3)
    print("Se estableció correctamente la conexión")

def handle_connection(client_conection, direction):
    data_received = receive_client_request(client_conection, direction)
    server_conection = forward_client_request_to_server(data_received)
    server_response = get_server_response(server_conection)
    send_server_response_to_client(client_conection, server_response)

def receive_client_request(client_conection, direction):
    print(f'Conectado {direction[0]}:{direction[1]}')
    return recieve_message(client_conection)

def forward_client_request_to_server(data_received):
    server_conection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_conection.connect(((SERVER_IP, SERVER_PORT)))
    server_conection.sendall(data_received)
    return server_conection

def get_server_response(server_conection):
    server_response = recieve_message(server_conection)
    server_conection.close()
    return server_response

def send_server_response_to_client(client_conection, server_response):
    client_conection.sendall(server_response)
    print('Desconectado')
    client_conection.close()

def recieve_message(receive_socket):
    initial_message = get_initial_message(receive_socket)
    head = get_header(initial_message)
    size = get_content_length_field(head)
    message = get_rest_of_message(receive_socket, initial_message, size)
    return message

def get_initial_message(receive_socket):
    BUFF_SIZE = 8192
    initial_message = receive_socket.recv(BUFF_SIZE)
    return initial_message

def get_header(initial_message):
    return initial_message[:find_bytes_in_bytes(initial_message, HTTP_HEADER_DELIMITER)]

def get_content_length_field(head):
    start = find_bytes_in_bytes(head, CONTENT_LENGTH_FIELD)
    if start == -1:
        return len(head)
    start += len(CONTENT_LENGTH_FIELD)
    end = find_bytes_in_bytes(head, b'\r\n', start)
    print(head[start:end].decode())
    return len(head) + int(head[start:end].decode())

def find_bytes_in_bytes(bytes, search_bytes, start=0):
    for i in range(start, len(bytes)):
        if bytes[i:i+len(search_bytes)] == search_bytes:
            return i
    return -1

def get_rest_of_message(receive_socket, initial_message, size):
    BUFF_SIZE = 8192
    data = initial_message
    while size - len(data) > 0:
        packet = receive_socket.recv(BUFF_SIZE)
        data += packet
        print(size, len(data))
    print(data)
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
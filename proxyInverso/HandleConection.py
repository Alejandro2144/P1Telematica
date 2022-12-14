import socket
from Cache import LRUCache
from ReceiveHTTP import receive_message
from methods import log, get_file

cache = LRUCache()

def handle_connection(client_conection, direction, SERVER_IP, SERVER_PORT):
    try:
        read_connection_and_return_response(client_conection, direction, SERVER_IP, SERVER_PORT)
    except socket.error or ConnectionRefusedError as exc:
        log(exc)
        manage_error(client_conection)

def read_connection_and_return_response(client_conection, direction, SERVER_IP, SERVER_PORT):
    data_received = receive_client_request(client_conection, direction)
    server_response  = cache.get(data_received)
    if server_response == None:
        server_conection = forward_client_request_to_server(data_received, SERVER_IP, SERVER_PORT )
        server_response = get_server_response(server_conection)
        file = get_file(server_response)
        cache.insert(data_received, file, len(file))
    send_server_response_to_client(client_conection, server_response)

def receive_client_request(client_conection, direction):
    log(f'Conectado {direction[0]}:{direction[1]}')
    received_message = receive_message(client_conection)
    log(received_message)
    return received_message

def forward_client_request_to_server(data_received, SERVER_IP, SERVER_PORT):
    server_conection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_conection.connect(((SERVER_IP, SERVER_PORT)))
    server_conection.sendall(data_received)
    log('Server ' + SERVER_IP + ':' + str(SERVER_PORT))
    return server_conection

def get_server_response(server_conection):
    server_response = receive_message(server_conection)
    log(server_response)
    server_conection.close()
    return server_response

def send_server_response_to_client(client_conection, server_response):
    client_conection.sendall(server_response)
    log('Desconectado')
    client_conection.close()

def manage_error(client_conection):
    internal_error = b'HTTP/1.1 500 Internal Server Error'
    log(internal_error)
    client_conection.sendall(internal_error)
    client_conection.close()
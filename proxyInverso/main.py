import socket
import threading
import constants
from methods import logger, log
from HandleConection import handle_connection, cache

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    try:
        server_setup()
        run_server()
    except Exception as exc:
        print(exc)
        logger.critical(exc)
    server_socket.close()

def server_setup():
    server_socket.bind((constants.SERVERS_PRIVATE_IP, constants.PORT))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.listen(3)
    log("Se estableció correctamente la conexión")

def select_server(current_server):
    SERVER_IP, SERVER_PORT = constants.SERVERS[current_server]
    current_server = (current_server + 1) % len(constants.SERVERS)
    return (SERVER_IP, SERVER_PORT, current_server)

def update_cache():
    while True:
        cache.update()

def run_server():
    current_server = 0
    cache_thread = threading.Thread(target=update_cache, args=())
    cache_thread.start()
    while True:
        socket_conection, direction = server_socket.accept()
        SERVER_IP, SERVER_PORT, current_server = select_server(current_server)
        client_thread = threading.Thread(target=handle_connection, args=(socket_conection,direction, SERVER_IP, SERVER_PORT))
        client_thread.start()

if __name__ == "__main__":
    main()
import constants
from methods import find_bytes_in_bytes, get_header

def receive_message(receive_socket):
    initial_message = get_initial_message(receive_socket)
    head = get_header(initial_message)
    size = get_content_length_field(head)
    message = get_rest_of_message(receive_socket, initial_message, size)
    return message

def get_initial_message(receive_socket):
    initial_message = receive_socket.recv(constants.BUFF_SIZE)
    return initial_message

def get_content_length_field(head):
    CONTENT_LENGTH_FIELD = b'Content-Length: '
    start = find_bytes_in_bytes(head, CONTENT_LENGTH_FIELD)
    if start == -1:
        return len(head)
    start += len(CONTENT_LENGTH_FIELD)
    end = find_bytes_in_bytes(head, b'\r\n', start)
    return len(head) + int(head[start:end].decode())

def get_rest_of_message(receive_socket, initial_message, size):
    data = initial_message
    while size - len(data) > 0:
        packet = receive_socket.recv(constants.BUFF_SIZE)
        data += packet
    return data

import socket
import constants

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Se estableció correctamente la conexión")

client_socket.connect(("localhost", constants.PORT))
print("Socket establecido")
command = ''
while command != constants.QUIT:
    command = input()
    client_socket.send(bytes(command, constants.ENCONDING_FORMAT))

print('Socket cerrado')
client_socket.close() 

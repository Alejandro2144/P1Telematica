import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Se estableció correctamente la conexión")

client_socket.connect(("localhost", 8080))
print("Socket establecido")
command = ''
while command != 'quit':
    command = input()
    client_socket.send(bytes(command, 'utf-8'))

print('Socket cerrado')
client_socket.close() 

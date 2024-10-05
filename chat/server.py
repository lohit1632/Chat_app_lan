import socket
import threading
from datetime import datetime

clients = {}

def handle_client(client_socket):
    username = client_socket.recv(1024).decode('utf-8')
    clients[client_socket] = username
    print(f"{username} has joined the chat!")

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast(format_message(username, message), client_socket)
        except:
            break
    
    print(f"{username} has left the chat!")
    client_socket.close()
    del clients[client_socket]

def format_message(username, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"[{timestamp}] {username}: {message}"

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.send(message.encode('utf-8'))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print("Server started! Waiting for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr} has been established!")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()

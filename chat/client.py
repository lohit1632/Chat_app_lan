import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            break

def format_message(message):
    if message.startswith('/bold'):
        return f"\033[1m{message[6:]}\033[0m"  # Bold text
    elif message.startswith('/italic'):
        return f"\033[3m{message[8:]}\033[0m"  # Italic text
    return message

def start_client(server_ip, username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, 12345))
    
    # Send the username to the server
    client.send(username.encode('utf-8'))

    threading.Thread(target=receive_messages, args=(client,)).start()

    while True:
        message = input()
        formatted_message = format_message(message)
        client.send(formatted_message.encode('utf-8'))

if __name__ == "__main__":
    server_ip = input("Enter server IP address: ")  # e.g., '192.168.1.5'
    username = input("Enter your username: ")
    start_client(server_ip, username)

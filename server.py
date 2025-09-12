import socket
import threading
import time

clients = []
nicknames = {}

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    nickname = "Anonymous"
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg.startswith("/nick "):
                nickname = msg.split(" ", 1)[1]
                nicknames[client] = nickname
                client.send(f"Nickname set to {nickname}\n".encode())
            elif msg.startswith("/msg "):
                text = msg.split(" ", 1)[1]
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                log_line = f"[{timestamp}] {nickname}: {text}\n"
                broadcast(log_line.encode())
                with open("chat.log", "a") as log:
                    log.write(log_line)
            else:
                client.send("Unknown command.\n".encode())
        except:
            clients.remove(client)
            client.close()
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen()
    print("Server started on port 12345.")
    while True:
        client, addr = server.accept()
        print(f"Connected with {addr}")
        clients.append(client)
        nicknames[client] = "Anonymous"
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    main()
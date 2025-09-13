import socket, select

HOST = "0.0.0.0"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"Server running on {HOST}:{PORT}")

sockets = [server]
clients = {}

while True:
    ready, _, _ = select.select(sockets, [], [])
    for sock in ready:
        if sock is server:
            conn, addr = server.accept()
            sockets.append(conn)
            clients[conn] = addr
            print(f"{addr} connected")
        else:
            data = sock.recv(1024)
            if not data:
                print(f"{clients[sock]} disconnected")
                sockets.remove(sock)
                del clients[sock]
                sock.close()
            else:
                msg = data.decode().strip()
                print(f"{clients[sock]}: {msg}")
                for s in sockets:
                    if s not in (server, sock):
                        s.sendall(data)
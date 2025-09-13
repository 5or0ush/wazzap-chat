import socket, select

HOST = "0.0.0.0"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print(f"Server running on {HOST}:{PORT}")

sockets = [server]

users = {}
next_id = 1

while True:
    ready, _, _ = select.select(sockets, [], [])
    for sock in ready:
        if sock is server:
            conn, addr = server.accept()
            sockets.append(conn)
            
            uname = f"user{next_id}"
            next_id += 1
            users[conn] = uname
            print(f"{addr} connected as {uname}")
            
            try:
                conn.sendall(f"SYS: welcome {uname}. Use /nick NAME to change your name.\n".encode())
            except:
                pass
            for s in sockets:
                if s not in (server, conn):
                    try:
                        s.sendall(f"SYS: {uname} joined\n".encode())
                    except:
                        pass
        else:
            data = sock.recv(1024)
            if not data:
                uname = users.get(sock, "unknown")
                print(f"{uname} disconnected")
                sockets.remove(sock)
                users.pop(sock, None)
                sock.close()
                for s in sockets:
                    if s is not server:
                        try:
                            s.sendall(f"SYS: {uname} left\n".encode())
                        except:
                            pass
                continue
            text = data.decode(errors="ignore").strip()
            uname = users.get(sock, "unknown")
            if text.startswith("/nick "):
                new = text.split(" ", 1)[1].strip()[:20]
                if not new:
                    try:
                        sock.sendall(b"SYS: usage /nick NAME\n")
                    except:
                        pass
                else:
                    old = uname
                    users[sock] = new
                    msg = f"SYS: {old} is now {new}"
                    print(msg)
                    for s in sockets:
                        if s is not server:
                            try:
                                s.sendall((msg + "\n").encode())
                            except:
                                pass
            else:
                
                wire = f"{uname}: {text}\n".encode()
                print(f"{uname}: {text}")
                for s in sockets:
                    if s not in (server, sock):
                        try:
                            s.sendall(wire)
                        except:
                            pass

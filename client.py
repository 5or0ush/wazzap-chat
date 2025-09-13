import socket, threading, sys

HOST = "127.0.0.1"
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def listen():
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(data.decode().strip())

threading.Thread(target=listen, daemon=True).start()

try:
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        sock.sendall(line.encode())
except KeyboardInterrupt:
    pass
finally:
    sock.close()
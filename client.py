import socket
import threading

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            print(msg)
        except:
            print("Disconnected from server.")
            break

def main():
    host = input("Enter server IP: ")
    port = int(input("Enter server port: "))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    thread = threading.Thread(target=receive, args=(sock,))
    thread.start()

    while True:
        msg = input()
        sock.send(msg.encode())

if __name__ == "__main__":
    main()
import socket

host, port = 'localhost', 9999


def recv_all(socketobj, filename, filesize):
    f = open(filename, "wb")
    while filesize > 0:
        if filesize < 1024:
            f.write(socketobj.recv(1024))
            break
        else:
            f.write(socketobj.recv(1024))
            filesize -= 1024
    f.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    sock.send(bytes("connect", encoding="utf-8"))
    print(str(sock.recv(1024), "utf-8"))
    while True:
        data = input()

        sock.sendall(bytes(data + "\n", "utf-8"))

        received = str(sock.recv(1024), "utf-8")
        print("Sent:     {}".format(data))
        print("Received: {}".format(received))

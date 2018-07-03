import socket
import time


class FileTransProgram(object):
    def __init__(self, ADDR, file_name):
        self.ADDR = ADDR
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(ADDR)
        self.file_name = file_name

    def recv(self):
        self.sock.send(bytes("Connect", "utf8"))
        file_size = self.sock.recv(1024).strip()
        with open(self.file_name, "wb") as f:
            while file_size > 0:
                if file_size < 1024:
                    f.write(self.sock.recv(1024))
                    break
                else:
                    f.write(self.sock.recv(1024))
                    file_size -= 1024
        self.sock.send(bytes("Success", "utf-8"))
        self.close()

    def stor(self):
        try:
            with open(self.file_name, "rb") as f:
                data = f.read()
                self.sock.send(bytes(str(len(data)), "utf-8"))
                time.sleep(0.2)
                self.sock.send(data)
        except FileNotFoundError as e:
            raise e
        ACK = str(self.sock.recv(1024).strip(), "utf-8")
        if ACK == "Success":
            self.close()

    def close(self):
        self.sock.close()

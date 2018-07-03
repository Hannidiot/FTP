import socket


class SocketCore(object):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isConnected = False
        self.num_of_none_pack = 0

    def connect(self, ADDR):
        try:
            self.sock.connect(ADDR)
            self.isConnected = True
        except socket.error as e:
            print("*** Fail to connect ***")
            print(e)

    def recv(self):
        data = bytes("", 'utf-8')
        while not data.endswith(bytes("\r\n", "utf-8")):
            data += self.sock.recv(1024)

        if data is None:
            self.exit_detect()
        elif self.num_of_none_pack:
            self.reset_num_of_none_pack()

        data = str(data[:-2], "utf-8")

        return data

    def send(self, msg):
        self.sock.sendall(bytes(msg + '\r\n', "utf-8"))

    def finish(self):
        self.sock.close()

    def exit_detect(self):
        self.num_of_none_pack += 1
        if self.num_of_none_pack >= 5:
            self.isConnected = False

    def reset_num_of_none_pack(self):
        self.num_of_none_pack = 0


class ReceiverThread(object):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ADDR):
        try:
            self.sock.connect(ADDR)
        except socket.error as e:
            print("*** Fail to connect ***")
            print(e)

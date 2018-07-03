from src.SocketCore import SocketCore
from src.DownloadProgram import *


class CmdLineProgram(object):
    def __init__(self, ADDR):
        self.address = ADDR

        self.username = "no user"
        self.sock = SocketCore()
        self.connected = None

    def run(self):
        self.sock.connect(self.address)
        self.sock.send("Connect Request")
        print(str(self.sock.sock.recv(1024), "utf-8"))
        while self.sock.isConnected:
            msg = str(input("{}({})> ".format(self.username, self.address[0])))
            self.sock.send(msg)
            data = self.sock.recv()
            cmd, arg = data.split(" ", maxsplit=1)
            try:
                func = getattr(self, "_" + cmd)
                func(arg)
            except AttributeError:
                self.default_func(arg)

    def _125(self, arg):
        pass

    @staticmethod
    def default_func(arg):
        print(arg)

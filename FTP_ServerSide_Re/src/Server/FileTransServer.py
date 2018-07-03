import socketserver
import time

from src.utility.Log import logger


class FileTransServer(socketserver.TCPServer):
    """
        Inherited form TCPServer
        用来实现启动文件传输服务器时向handler方法传file_path参数
    """
    def __init__(self, server_address, RequestHandlerClass, file_path, file_size, bind_and_activate=True):
        self.file = file_path
        self.file_size = file_size
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self.file, self.file_size)


class DownloadHandler(socketserver.StreamRequestHandler):
    def __init__(self, request, client_address, server, file_path, file_size):
        self.file = file_path
        self.file_size = file_size
        super().__init__(request, client_address, server)

    def handle(self):
        self.request.recv(1024)
        try:
            with open(self.file, 'rb') as f:
                data = f.read()
                self.request.send(bytes(self.file_size, encoding="utf-8"))
                time.sleep(0.2)
                self.request.send(data)
        except FileNotFoundError:
            logger.error("{} not found", self.file)

        end = str(self.request.recv(1024).strip(), "utf-8")
        if end == "Success":
            self.finish()

    def finish(self):
        self.server.shutdown()
        self.request.close()


class RecvHandler(socketserver.StreamRequestHandler):
    def __init__(self, request, client_address, server, file_path, file_size=None):
        self.file = file_path
        self.file_size = file_size
        super().__init__(request, client_address, server)

    def handle(self):
        fn = str(self.request.recv(1024).strip(), 'utf-8')
        fz = int(self.request.recv(1024).strip(), 'utf-8')
        f = open(self.file + "/" + fn, 'wb')
        while fz > 0:
            if fz < 1024:
                f.write(self.request.recv(1024))
                break
            else:
                f.write(self.request.recv(1024))
                fz -= 1024
        f.close()

        self.request.send(bytes("Success", "utf-8"))
        self.finish()

    def finish(self):
        self.server.shutdown()
        self.request.close()

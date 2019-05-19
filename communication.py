import socket
import message_util


class ComSupervisor:
    def __init__(self, addr, port):
        self.port = port
        self.addr = addr

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect((self.addr, self.port))
        except ConnectionRefusedError:
            return False

        return True

    def send(self, send):
        message_util.send_msg(self.socket, send)
        data = message_util.recv_msg(self.socket)

        print("Received", data)

    def get_info(self):
        return self.addr, self.port

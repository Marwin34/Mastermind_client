import select
import socket
import message_util
from conn_conf import conf_addr, conf_port


class ComSupervisor:
    def __init__(self):
        self.port = conf_port
        self.addr = conf_addr

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connected = False

    def connect(self):
        try:
            self.socket.connect((self.addr, self.port))
        except ConnectionRefusedError:
            self.connected = False
            return False

        self.connected = True
        return True

    def send(self, send):
        message_util.send_msg(self.socket, send)

    def receive(self):
        ready_to_read, ready_to_write, in_error = select.select([self.socket], [], [], 0.01)
        if self.socket in ready_to_read:
            data = message_util.recv_msg(self.socket)

            return data

        return None

    def get_info(self):
        return self.addr, self.port, self.connected

import socket


class UDP_socket:
    def __init__(self, UDP_IP_ADRESS="127.0.0.1", port=63, tx=0):
        self.udp_ip_address = UDP_IP_ADRESS
        self.tx = tx
        self.port = port
        self.setup()

    def setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if not self.tx:
            self.socket.bind((self.udp_ip_address, self.port))

    def receive(self):
        data, addr = self.socket.recvfrom(1024)
        return data.decode(), addr

    def send(self, message):
        self.socket.sendto(message.encode(), (self.udp_ip_address, self.port))

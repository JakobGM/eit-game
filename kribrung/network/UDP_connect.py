import socket

class UdpSocket:
    def __init__(self, ip_address="0.0.0.0", port=2055, tx=0):
        # Initiate values
        self.socket = None

        self.udp_ip_address = ip_address
        self.tx = tx
        self.port = port
        self.setup()

    def setup(self):
        """
        Sets up the socket.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if not self.tx:
            self.socket.bind((self.udp_ip_address, self.port))

    def receive(self, data_size=1024):
        """
        Receives message from socket
        :return: A message received from the socket
        """
        data, addr = self.socket.recvfrom(data_size)
        return data.decode(), addr

    def send(self, message):
        """
        Sends a message to the socket.
        :param message: A messages to be sent to the socket
        """
        self.socket.sendto(message.encode(), (self.udp_ip_address, self.port))

    def close_connection(self):
        """
        Closes the established connection.
        Needs to be called if it is a TCP connection or a receiving UDP connection.
        """
        self.socket.close()

from UDP_connect import UdpSocket
receive = UdpSocket(ip_address = "0.0.0.0", port=2055) ##uses
print_ct = 0
x = 0
y = 0

while 1:
   gyro_data, user_data = receive.receive()
   coor = list(map(lambda x: float(x), gyro_data[:-1].split(',')))
   x, y = -coor[1], -coor[0]
   print_ct += 1

   if print_ct > 50:
      print_ct = 0
      print("x: {} y: {}".format(x, y))

class connect_phone:

    def __init__(self, port):

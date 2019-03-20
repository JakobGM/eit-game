"""Phone and UDP socket."""
import socket
import numpy as np


class UdpSocket:
    """An udp socket."""

    def __init__(self, ip_address: str = "0.0.0.0", port: int = 2055,
                 tx: bool = False) -> None:
        r"""
        Set up a general UDP socket that can be a client or server.

        :param ip_address: The ip address for outbound or inbound packets
        :param port: The port for outbound or inbound packets
        :param tx: 0 if the socket only receives packets, \
        or 1 if it only sends.
        """
        # Initiate values
        self.socket: socket.Socket = None

        self.udp_ip_address: str = ip_address
        self.tx: bool = tx
        self.port: int = port
        self.setup()

    def setup(self) -> None:
        """Set up the socket."""
        self.socket: socket.Socket = \
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if not self.tx:
            self.socket.bind((self.udp_ip_address, self.port))

    def receive(self, data_size: int = 1024) -> (str, str):
        """
        Receives message from socket.

        :return: A message received from the socket
        """
        data, addr = self.socket.recvfrom(data_size)
        return data.decode(), addr

    def send(self, message: str) -> None:
        """
        Send a message to the socket.

        :param message: A messages to be sent to the socket
        """
        self.socket.sendto(message.encode(), (self.udp_ip_address, self.port))

    def close_connection(self) -> None:
        r"""
        Close the established connection.

        Needs to be called if it is a TCP connection or a receiving UDP \
        connection.
        """
        self.socket.close()


class ConnectPhone:
    """A class representing a phone."""

    def __init__(self, coor=0, gyro_data=0, port=2055, x=0, y=0, z=0,
                 print_ct=0):
        """Initialize the phone."""
        self.x = x
        self.y = y
        self.z = z
        self.print_ct = print_ct
        self.coor = coor
        self.gyro_data = gyro_data
        self.port = port
        self.ready = False

    def set_up(self):
        """Set up a phone."""
        self.udp_socket = UdpSocket(port=self.port)
        self.ready = True

    def vect_phone(self):
        """Get value from the phone."""
        self.gyro_data, self.user_data = self.udp_socket.receive()
        self.coor = list(
            map(lambda x: float(x), self.gyro_data[:-1].split(",")))
        self.x, self.y, self.z = -self.coor[1], -self.coor[0], self.coor[2]
        # make the z a bool
        return np.array([self.x, self.y])

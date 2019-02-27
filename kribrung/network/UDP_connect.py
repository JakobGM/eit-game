import socket
import numpy as np
import pygame as pg
import time


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


class connect_phone:
    def __init__(self, coor=0, gyro_data=0, port=2055, x=0, y=0, z=0, print_ct=0):
        self.port = port
        self.x = x
        self.y = y
        self.z = z
        self.print_ct = print_ct
        self.coor = coor
        self.gyro_data = gyro_data
        self.udp_socket = UdpSocket(port=self.port)

    def vect_phone(self):
        """
        supposed to be used as a input to the game.
        :return: Returns a description of the phone's orientation
        """
        is_flipped = False
        phone = self.udp_socket
        self.gyro_data, self.user_data = phone.receive()
        self.coor = list(map(lambda x: float(x), self.gyro_data[:-1].split(",")))
        self.x, self.y, self.z = -self.coor[1], self.coor[0], self.coor[2]
        if self.z < -5:
            is_flipped = True
        return np.array([self.x/10, self.y/10]), is_flipped

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
      print("x: {} y: {}".format(x, y))
      print_ct = 0

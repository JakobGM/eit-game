from UDP_connect import UDP_socket
receive = UDP_socket(UDP_IP_ADRESS = "0.0.0.0", port=2055)
while 1:
   gyro_data, user_data = receive.receive()
   coor = list(map(lambda x: x[:-5], gyro_data.split(',')))
   print("x: {} y: {} z: {}".format(coor[0],coor[1],coor[2]))


"""
<Program Name>
  affix_python_tcp_benchmark_send.py

<Purpose>
  This is a test file that will be used for benchmarking
  tcp connectivity over the sender using 
  different data blocks.

<Usage>
  $ python affix_python_tcp_benchmark_send.py packet_block_size(in KB) total_data_to_send(in MB)
"""
import sys
import time
import threading
import random
import socket

# 1KB string size.
random_string = 'a'
#random_string = 'abcdefgh' * 128

block_size = 1024 
start_time = 0

FIN_TAG="@FIN"
total_data_sent = 0

port = 12347
server_address = '192.168.0.111'


def main():
  """
  <Purpose>
    The main thread is the client that sends data across to 
    the server across the loopback address.
  """
  global block_size
  global start_time
  global total_data_sent

  if len(sys.argv) < 3:
    print "  $ python affix_python_tcp_benchmark.py packet_block_size(in KB) total_data_to_send(in MB)"
    sys.exit(1)

  # Extract the user input to figure out what the block size will be 
  # and how much data to send in total.
  block_size = int(sys.argv[1])
  data_length = int(sys.argv[2]) * 1024 * 1024

  repeat_data = random_string * block_size
  
  total_sent = 0

  # Create a client socket and connect to the server. Following
  # the connection, send data repeatedly until we have sent
  # sufficient ammount.
  sockobj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  start_time = time.time()
  # print start_time
  start_time_string = "%f" %start_time
  # print start_time_string
  time_len =  len(start_time_string)
  sockobj.sendto(start_time_string, (server_address, port))
  sockobj.sendto(" ", (server_address, port))
  total_data_sent = time_len + 1

  while total_data_sent < data_length:
    total_data_sent += sockobj.sendto(repeat_data, (server_address, port))
  # print total_data_sent

  # Send a signal telling the server we are done sending data.
  for i in range(10):
    sockobj.sendto(FIN_TAG, (server_address, port))

  sockobj.close()
  



if __name__ == '__main__':
  main()

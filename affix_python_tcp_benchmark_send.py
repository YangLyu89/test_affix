"""
<Program Name>
  affix_python_tcp_benchmark_send.py

<Purpose>
  This is a test file that will be used for benchmarking
  tcp connectivity on sender using 
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

port = 12346
server_address = '160.39.31.119'

def main():

  global block_size
  global start_time

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
  sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sockobj.connect((server_address, port))

  start_time = time.time()
  # print start_time
  start_time_string = "%f" %start_time
  time_len =  len(start_time_string)
  sockobj.send(start_time_string)
  sockobj.send(" ")
  total_sent = time_len + 1

  while total_sent < data_length:
    total_sent += sockobj.send(repeat_data)

  # Send a signal telling the server we are done sending data.
  sockobj.send(FIN_TAG)
  sockobj.close()
  

    









if __name__ == '__main__':
  main()

"""
<Program Name>
  affix_python_udp_benchmark_send.py

<Purpose>
  This is a test file that will be used for benchmarking
  udp connectivity over the sender using 
  different data blocks.

<Usage>
  $ python affix_repy_udp_benchmark_send.py packet_block_size(in KB) total_data_to_send(in MB)
"""
import sys
import time
import threading
import random
import socket

from repyportability import *
_context = locals()
add_dy_support(_context)

dy_import_module_symbols("affix_stack.r2py")


# 1KB string size.
random_string = 'a'
# random_string = 'abcdefgh' * 128

block_size = 1024 
start_time = 0
sleep_time = 0.00001

FIN_TAG="@FIN"
total_data_sent = 0

port = 12347
server_address = '192.168.0.111'


affix_string = '(NoopAffix)'


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
  block_multiplier = int(sys.argv[1])
  data_length = int(sys.argv[2]) * 1024 * 1024

  repeat_data = random_string * block_multiplier
  block_size = block_size * block_multiplier
  
  total_sent = 0


  # Send data repeatedly until we have sent
  # sufficient ammount through UDP.
  affix_obj = AffixStack(affix_string)

  start_time = time.time()
  myip = getmyip()

  start_time_string = "%f" %start_time
  # print start_time_string
  time_len =  len(start_time_string)
  total_data_sent = affix_obj.sendmessage(server_address, port, start_time_string, myip, port+1)
  total_data_sent += affix_obj.sendmessage(server_address, port, " ", myip, port+1)

  while total_data_sent < data_length:
    try:
      total_data_sent += affix_obj.sendmessage(server_address, port, repeat_data, myip, port+1)
    except SocketWouldBlockError:
      time.sleep(sleep_time)
      pass

  # print total_data_sent

  # Send a signal telling the server we are done sending data.
  affix_obj.sendmessage(server_address, port, FIN_TAG, myip, port+1)
  



if __name__ == '__main__':
  main()

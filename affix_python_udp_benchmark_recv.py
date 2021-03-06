"""
<Program Name>
  affix_python_tcp_benchmark_recv.py

<Purpose>
  This is a test file that will be used for benchmarking
  tcp connectivity over the receiver using 
  different data blocks.

<Usage>
  $ python affix_python_tcp_benchmark_recv.py
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
total_data_sent = 268435474

port = 12347
server_address = '192.168.0.111'

class server(threading.Thread):
  """
  <Purpose>
    The purpose of this thread is to only receive the
    message sent by the client and time it.
  """
  def __init__(self):
    threading.Thread.__init__(self)

  def run(self):
    # Create a new server socket and accept a connection when
    # there is an incoming connection.
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_server.bind((server_address, port))


    # Now that we have accepted the connection, we will 
    recv_msg = ''
    data_recv_len = 0

    temp_msg = sock_server.recvfrom(block_size)
    data_recv_len = len(temp_msg)
    start_time = float(temp_msg[0])

    while True:
      try:
        cur_msg, addr = sock_server.recvfrom(block_size)
        if FIN_TAG in cur_msg:
          break
        data_recv_len += len(cur_msg)
        recv_msg += cur_msg
      except socket.error:
        break

    total_run_time = time.time() - start_time
    
    print "Time to receive: %s" % str(total_run_time)
    print "Total data received: %d KB. \nThroughput: %s KB/s" % (data_recv_len/1024, str(data_recv_len/total_run_time/1024))

    total_data_loss = total_data_sent - data_recv_len
    print "Data loss: %d KB\nLoss rate: %s%%" % (total_data_loss/1024, str((total_data_loss*1.0/total_data_sent*100)))



def main():

  # Start the server then wait a few seconds before connecting.
  new_server = server()
  new_server.start()
  time.sleep(2)


if __name__ == '__main__':
  main()

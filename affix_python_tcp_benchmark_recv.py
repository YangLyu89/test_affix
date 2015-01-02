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

port = 12346
server_address = '160.39.31.119'

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
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_server.bind((server_address, port))
    sock_server.listen(5)

    # Accept each incoming connection and launch a new client
    # benchmark thread that will time how long it took to 
    # receive all the data.
    while True:
      (clientsocket, address) = sock_server.accept()
      print "Accepted conn from: " + str(address)
      break

    # Now that we have accepted the connection, we will 
    recv_start_time = time.time()
    
    # print recv_start_time


    temp_msg = clientsocket.recv(block_size)
    data_recv_len = len(temp_msg)
    start_time = float(temp_msg.split()[0])
    # print start_time
    # start_time = time.time()


    recv_msg = ''
    # data_recv_len = 0
    while True:
      try:
        cur_msg = clientsocket.recv(block_size)
        data_recv_len += len(cur_msg)
        if FIN_TAG in cur_msg:
          break
        recv_msg += cur_msg
      except socket.error:
        break

    total_recv_time = time.time() - recv_start_time
    total_run_time = time.time() - start_time
    
    print "Time to receive: %s\nTotal time: %s" % (str(total_recv_time), str(total_run_time))
    print "Total data received: %d KB. \nThroughput: %s KB/s" % (data_recv_len/1024, str(data_recv_len/total_run_time/1024))




def main():
  
  # Start the server then wait a few seconds before connecting.
  new_server = server()
  new_server.start()
  time.sleep(2)
  



if __name__ == '__main__':
  main()

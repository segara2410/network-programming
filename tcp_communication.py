import argparse
import os
import socket
import sys
import time

class TcpHandler():
  def __init__(self, role, host, port):
    if role == 'server':
      server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      server_socket.bind((host, port))
      server_socket.listen(1)
      print('Listening at', server_socket.getsockname())
      self.socket, sockname = server_socket.accept()
      print('We have accepted a connection from', sockname)
      print('  Socket name:', self.socket.getsockname())
      print('  Socket peer:', self.socket.getpeername())


    if role =='client':
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socket.connect((host, port))
      print('Client has been assigned socket name', self.socket.getsockname())


  def recvall(self, length):
    data = b''
    while len(data) < length:
      more = self.socket.recv(length - len(data))
      if not more:
        raise EOFError('was expecting %d bytes but only received'
                      ' %d bytes before the socket closed'
                      % (length, len(data)))
      data += more
    return data

  def receive_string(self):
    length = self.recvall(3)
    message = self.recvall(int(length)).decode("utf-8")

    return length, message

  def send_string(self, string):
    message = f'{len(string):03d}{string}'
    self.socket.sendall(str.encode(message))

class Server():
  def __init__(self, host, port):
    self.tcp_handler = TcpHandler('server', host, port)

  def list_dir(self, path):
    return os.listdir(path)

  def file_to_string(self, path):
    with open(path) as file:
      return file.read()

  def handle_command(self):
    _, command = self.tcp_handler.receive_string()

    parsed_command = command.split()

    if parsed_command[0] == 'ls':
      self.tcp_handler.send_string('\n'.join(self.list_dir(
        parsed_command[1] if len(parsed_command) > 1 else None)
      ))

    if parsed_command[0] == 'get':
      content = self.file_to_string(parsed_command[1])
      self.tcp_handler.send_string(content)

    if parsed_command[0] == 'quit':
      time.sleep(1)
      print('server shutdown..')
      quit()

class Client():
  def __init__(self, host, port):
    self.tcp_handler = TcpHandler('client', host, port)

  def string_to_file(self, string, path):
    with open(path, "w") as file:
      file.write(string)

  def handle_command(self, command):
    parsed_command = command.split()
    if parsed_command[0] == 'get':
      if len(parsed_command) < 3:
        print('please specify the target and destination files.')
        return

    if parsed_command[0] in ['ls', 'get', 'quit']:
      self.tcp_handler.send_string(command)

      if parsed_command[0] == 'quit':
        print('server shutdown..')
        print('client shutdown..')
        quit()
      
      length, response = self.tcp_handler.receive_string()
      if parsed_command[0] == 'ls':
        print(response)

      if parsed_command[0] == 'get':
        print(f'fetch: {parsed_command[1]} size: {int(length)} lokal: {parsed_command[2]}')
        self.string_to_file(response, parsed_command[2])

    else:
      print('unknown command, please try again')


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Send and receive over TCP')
  parser.add_argument('role', choices=['client', 'server'], help='which role to play')
  parser.add_argument('host', help='interface the server listens at;'
                      ' host the client sends to')
  parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                      help='TCP port (default 1060)')

  args = parser.parse_args()
  if args.role == 'client':
    client = Client(args.host, args.p)

    while True:
      command = input('> ')
      client.handle_command(command)
  
  elif args.role == 'server':
    server = Server(args.host, args.p)

    while True:
      server.handle_command()

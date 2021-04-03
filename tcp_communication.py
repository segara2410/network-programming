import os
import socket
import sys

class TcpHandler():
  def __init__(self, role):
    # init self.socket here
    # if role == 'server':
    # else

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

  def receive_str(self):
    length = recvall(3)
    message = recvall(int(length)).decode("utf-8")

    return length, message

  def send_str(self, string):
    self.socket.sendall(str.encode(string))

class Server():
  def __init__(self):
    self.tcp_handler = TcpHandler('server')

  def list_dir(self, path):
    return os.listdir(path)

  def file_to_string(self, path):
    with open(path) as file:
      return file.read()

  def handle_command(self):
    #  _, command = self.tcp_handler.receive_str(content)

    parsed_command = command.split()
    if parsed_command[0] == 'ls':
      return self.list_dir(parsed_command[1] if len(parsed_command) > 1 else None)

    if parsed_command[0] == 'get':
      content = self.file_to_string(parsed_command[1])
      print(content)
      # send this later
      # self.tcp_handler.send_str(content)

    if parsed_command[0] == 'quit':
      quit()

class Client():
  def __init__(self):
    self.tcp_handler = TcpHandler('client')

  def string_to_file(self, string, path):
    with open(path, "w") as file:
      file.write(string)

  def handle_command(self, command):
    parsed_command = command.split()
    if command[0] in ['ls', 'get', 'quit']:
      # send this later
      # self.tcp_handler.send_str(content)

      if command[0] == 'quit':
        quit()
      
      # length, response = self.tcp_handler.receive_str(content)
      if command[0] == 'ls':
        print(response)

      if command[0] == 'get':
        print(f'fetch:{command[1]} size: {length} lokal:{command[2]}')
        string_to_file(response, command[2])

    else:
      print('unknown command, please try again')


if __name__ == '__main__':
  if len(sys.argv) > 1:
    if str(sys.argv[1]) == 'client':
      client = Client()

      while True:
        command = input('> ')
        client.handle_command()
    
    elif str(sys.argv[1]) == 'server':
      server = Server()

      while True:
        server.handle_command()

  else:
    print('invalid argument.')
import rpyc
import argparse


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='TCP Client Program')
  parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                      help='TCP port (default 1060)')

  args = parser.parse_args()
  print(f'Client running on port {args.p}')

  client = rpyc.connect("localhost", args.p)

  while True:
    command = input('> ').strip()
    if command.startswith('rawquery(\'') and command.endswith('\')'):
      query = command[command.find('\'') + 1:-2]
      print(client.root.rawquery(query))
    elif command.startswith('tabquery(\'') and command.endswith('\')'):
      query = command[command.find('\'') + 1:-2]
      print(client.root.tabquery(query))
    elif command == 'quit':
      client.root.quit()
    else:
      print('Invalid command!')

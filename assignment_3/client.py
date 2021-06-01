import rpyc

client = rpyc.connect("localhost", 2410)

while True:
  command = input('> ')
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

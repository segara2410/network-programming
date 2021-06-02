import rpyc
from rpyc.utils.helpers import classpartial
from rpyc.utils.server import ThreadedServer
from sqlite3 import Connection, Cursor, connect
from beautifultable import BeautifulTable
import argparse

class SqliteHandler():
  def __init__(self, database: str):
    self.connection: Connection = connect(database)
    self.cursor: Cursor = self.connection.cursor()

  def run_query(self, query: str) -> list:
    self.cursor.execute(query)

    return self.cursor.fetchall()


class SqliteHandlerService(rpyc.Service):
  def __init__(self, database: str):
    self.sqlite_handler = SqliteHandler(database)

  def exposed_rawquery(self, query: str) -> list:
    return self.sqlite_handler.run_query(query)

  def exposed_tabquery(self, query: str) -> str:
    result = self.sqlite_handler.run_query(query)

    table = BeautifulTable()
    for row in result:
      table.rows.append(row)

    table.rows.header = ["S"+str(i) for i in range(1, len(result) + 1)]
    table.columns.header = [description[0] for description in self.sqlite_handler.cursor.description]

    return table

  def exposed_quit(self) -> None:
    exit()


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='TCP Server Program')
  parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                      help='TCP port (default 1060)')
  parser.add_argument('-d', metavar='DATABASE', type=str, default='data.db',
                      help='Database (default data.db)')

  args = parser.parse_args()
  print(f'Server running on port {args.p} using {args.d}')
  service = classpartial(SqliteHandlerService, args.d)
  server = ThreadedServer(service, port=args.p)
  server.start()

import rpyc
from rpyc.utils.helpers import classpartial
from rpyc.utils.server import ThreadedServer
from sqlite3 import Connection, Cursor, connect
from beautifultable import BeautifulTable

class SqliteHandler():
  def __init__(self, database: str):
    self.connection: Connection = connect(database)
    self.cursor: Cursor = self.connection.cursor()

  def run_query(self, query: str) -> list:
    self.cursor.execute(query)

    return self.cursor.fetchall()


class MyService(rpyc.Service):
  def __init__(self, database: str):
    self.sqlite_handler = SqliteHandler(database)

  def exposed_rawquery(self, query: str) -> str:
    return str(self.sqlite_handler.run_query(query))

  def exposed_tabquery(self, query: str) -> str:
    result = self.sqlite_handler.run_query(query)

    table = BeautifulTable()
    for row in result:
      table.rows.append(row)

    table.rows.header = ["S"+str(i) for i in range(1, len(result) + 1)]
    table.columns.header = [description[0] for description in self.sqlite_handler.cursor.description]

    return table

  def exposed_quit(self):
    exit()


if __name__ == "__main__":
  service = classpartial(MyService, 'data.db')
  server = ThreadedServer(service, hostname='localhost', port=2410)
  server.start()

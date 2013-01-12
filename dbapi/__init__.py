import sqlite3
import os.path
import sys

print("Running setup lol")

def _setup():
  global conn
  if hasattr(_setup, 'done'):
    return

  # Fix import paths for dbapi
  # NOTE: This isn't particularly awesome, since multiple 'packages' like this
  # will all try to win. It might be fine if we just have dbapi.
  import_path = os.path.dirname(__file__)
  if import_path not in sys.path:
    sys.path.insert(0, import_path)

  # This is the directory of this file
  db_path = os.path.dirname(__file__)
  conn = sqlite3.connect(db_path + "/database.db")
  cur = conn.cursor()
  cur.executescript(open(db_path + "/setup.sql").read())

  _setup.done = True

_setup()

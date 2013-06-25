import os
import json
from collections import defaultdict


class SearchIndex(object):
    def __init__(self, identifier, index=None):
        self.identifier = identifier
        self.non_json_index = index if type(index) == defaultdict else None
        self.json_index = json.dumps(index) if type(index) == dict else index

    @property
    def index(self):
        if not self.non_json_index:
            self.non_json_index = json.loads(self.json_index)
            return self.non_json_index
        else:
            return self.non_json_index

    @index.setter
    def index_setter(self, index):
        if type(index) == dict:
            self.non_json_index = index
        else:
            self.non_json_index = json.loads(index)
            self.json_index = index

    @classmethod
    def create(*args):
        return SearchIndex(*args)

    @classmethod
    def all(self, cursor):
        query = 'SELECT * FROM SearchIndex'
        cursor.execute(query)
        index_models = [SearchIndex(*q) for q in cursor.fetchall()]
        return index_models

    def put(self, cursor, conn):
        if type(self.json_index) != str:
            self.json_index = json.dumps(self.non_json_index)

        cursor.execute(
            'INSERT INTO SearchIndex VALUES (?, ?)',
            (self.identifier, self.json_index))
        conn.commit()


def create_table(conn, if_exists=False):
    if if_exists:
        conn.execute('DROP TABLE IF EXISTS SearchIndex')
    conn.execute(open(
        os.path.join('dbapi', 'setup_tables', 'searchindex.sql')).read())
    conn.commit()

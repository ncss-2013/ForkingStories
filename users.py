import sqlite3
conn = sqlite3.connect("something.db")

def nuke():
    conn.execute("DROP TABLE IF EXISTS users;")


class User(object):
    def __init__(self, uid, fname, lname, username, password):

        self.uid = uid
        self.fname = fname
        self.lname = lname
        self.username = username
        self.password = password

    def get(username):
        cur = conn.cursor()
        cur.executescript(open("something.sql").read())
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        for row in cur:
            return row


    def create(uid, fname, lname, username, password):
        cur = conn.cursor()
        cur.executescript(open("something.sql").read())
        cur.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?, ?);",
            (uid, fname, lname, username, password))

    def put(fieldname, value):
        #cur = conn.cursor()
        #cur.executescript(open("something.sql").read())
        #cur.execute()
        if something is None:
            pass
        pass
        


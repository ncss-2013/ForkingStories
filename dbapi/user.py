from __init__ import *

def nuke():
    conn.execute("DROP TABLE IF EXISTS users;")


class User(object):
    def __init__(self, uid, fname, lname, username, password):

        self.uid = uid
        self.fname = fname
        self.lname = lname
        self.username = username
        self.password = password

    @classmethod
    def get(cls, username):
        cur = conn.cursor()
        cur.execute("SELECT id, firstname, lastname, username, password FROM users WHERE username = ?",
                    (username,))
        for row in cur:
            return User(*row)

    def create(uid, fname, lname, username, password):
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?, ?);",
            (uid, fname, lname, username, password))

    def update(self, fieldname, value):
        cur = conn.cursor()
        cur.execute("UPDATE users SET " + fieldname + "=? WHERE id = ?",
                    (value, self.uid))

    def put(self):
        self.update('firstname', self.fname)
        self.update('lastname', self.lname)
        self.update('password', self.password)
        #User name and id can't change

if __name__ == "__main__":
    #the test code
    s = User.get('sdfko')
    previous_name = s.fname
    s.fname = "Sam"
    s.put()
    s2 = User.get('sdfko')
    assert s2.fname != previous_name, "Name didn't change :("

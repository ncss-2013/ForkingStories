import __importfix__; __package__ = 'dbapi'
from .__init__ import *
import dbapi.dbtime as dbtime

def nuke():
    conn.execute("DROP TABLE IF EXISTS users;")

class RecordNotFound(Exception):
    pass

class UsernameAlreadyExists(Exception):
    pass

class User(object):
    def __init__(self, uid, fname, lname, username, password, dob, email, joindate):
        self.uid = uid
        self.fname = fname
        self.lname = lname
        self.username = username
        self.password = password
        self.dob = dob
        self.email = email
        self.joindate = joindate

    @classmethod
    def get(cls, field_name:str, query:str=""):
        """
        Arguments required, in order: the query (what the user is searching for), and the field name of the field they are searching in.
        """
        cur = conn.cursor()
        if field_name == "all":
            cur.execute("SELECT id, fname, lname, username, password, dob, email, joindate FROM users")
        else:
            cur.execute("SELECT id, fname, lname, username, password, dob, email, joindate FROM users WHERE " + field_name + " = ?",
                    (query,))
        rows = cur.fetchall()
        results = []
        for row in rows:
            results.append(User(*row))
        print(str(len(results)) + " result(s) found.")
        if len(results) == 1:
            return User(*row)
        elif len(results) == 0:
            raise RecordNotFound
        else:
            return results
    #You can't edit the results of this query unless there is only 1 unique result, so if you search username or uid

    def create(fname, lname, username, password, dob, email):
        joindate = 0.3253
        #TODO put method for date here
        return User(None, fname, lname, username, password, dob, email, joindate)
        
    #Don't use update, but don't delete it either!!!
    def update(self, fieldname, value):
        cur = conn.cursor()
        cur.execute("UPDATE users SET "+ fieldname +" = ? WHERE id = ?",
                    (value, self.uid))

    def save(self):
        if self.uid is None:
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE username = ?",(self.username,))
            rows = cur.fetchall()
            results = []
            for row in rows:
                results.append(User(*row))
            if results:
                raise UsernameAlreadyExists()
            else:
                cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (self.uid, self.fname, self.lname, self.username, self.password, self.dob, self.email, self.joindate))
        else:
            self.update('fname', self.fname)
            self.update('lname', self.lname)
            self.update('password', self.password)
            self.update('id', self.uid)
            self.update('email', self.email)
        conn.commit()
        #User name and id can't change

    def delete(self):
        cur = conn.cursor()
        cur.execute('''DELETE FROM users
                    WHERE id = ?''', (self.uid,))
        conn.commit()



if __name__ == "__main__":
    s = User.get('username', 'Melogh24')
    previous_name = s.fname
    if s.fname == "Melissa":
        s.fname = "SZam"
    else:
        s.fname = "Melissa"
    s.save()
    s2 = User.get('username', 'Melogh24')
    assert s2.fname != previous_name, "Name didn't change :("        

    #help(User.get)

   

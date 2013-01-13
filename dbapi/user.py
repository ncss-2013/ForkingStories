#!/usr/bin/env python3
'''user.py

Contains a User object to interface with the user table in the database.

Written by Melissa McKeogh and Jessica Zhang

'''

import __importfix__; __package__ = 'dbapi'
from .__init__ import *
import math
import dbapi.dbtime as dbtime
from dbapi.paragraph import Paragraph as Paragraph
#from dbapi.story import Story
import dbapi.story

def nuke():
    conn.execute("DROP TABLE IF EXISTS users;")
    conn.execute("DROP TABLE IF EXISTS stories;")
    conn.execute("DROP TABLE IF EXISTS paragraphs;")

class UsernameAlreadyExists(Exception):
    pass

class User(object):
    '''This class represents a row in the user table.

Use User.find(<fieldname for query>, <some query>) to fetch a list
of User objects representing rows in the user table.

Use User.create(fname, lname, username, password, year, month, day, email, location, bio) to create a new User object.
Id, joindate are created automatically. Dob is figured from the year, month, day.

Use User.save() to add the user row to the database.

To delete a User from the database, find the user then use User.delete()
e.g. u = User.find(<fieldname>, <value>)
     u.delete()

for the rest of these explanations, u is a user object.

Use u.get_contributed_stories() to return a list of Story objects the User has contributed to.

Use u.get_stories() to return a list of Story objects the User has created.

Use u.get_number_of_stories() to return an integer representing the number of Story objects the User has created.

Use u.get_number_of_paragraphs() to return an integer representing the number of paragraphs the User has contributed overall.

Use u.get_number_of_paragraphs_approved() to return an integer representing the number of paragraphs the User has contributed that have been approved.

'''
    
    def __init__(self, uid, fname, lname, username, password, dob, email, joindate, location, bio):
        self.id = uid
        self.fname = fname
        self.lname = lname
        self.username = username
        self.password = password
        self.dob = dob
        self.email = email
        self.joindate = joindate
        self.location = location
        self.bio = bio

    @classmethod
    def find(cls, field_name:str, query:str = ""):
        """
        Arguments required, in order: the query (what the user is searching for), and the field name of the field they are searching in.
        """
        cur = conn.cursor()
        if field_name == "all":
            cur.execute("SELECT id, fname, lname, username, password, dob, email, joindate, location, bio FROM users")
        else:
            cur.execute("SELECT id, fname, lname, username, password, dob, email, joindate, location, bio FROM users WHERE " + field_name + " = ?",
                    (query,))
        rows = cur.fetchall()
        results = []
        for row in rows:
            results.append(User(*row))
        return results
    #When you edit, use User.find()[0] (you can't edit multiple results, it will just edit the first one)

    def create(fname, lname, username, password, year, month, day, email, location, bio):
        joindate = dbtime.make_time_str()
        dob = dbtime.make_time_str((int(year), int(month), int(day)))
        return User(None, fname, lname, username, password, dob, email, joindate, location, bio)
        
    #Don't use update, but don't delete it either!!!
    def update(self, fieldname, value):
        cur = conn.cursor()
        cur.execute("UPDATE users SET "+ fieldname +" = ? WHERE id = ?",
                    (value, self.id))

    def save(self):
        if self.id is None:
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE username = ?",(self.username,))
            rows = cur.fetchall()
            results = []
            for row in rows:
                results.append(User(*row))
            if results:
                raise UsernameAlreadyExists()
            else:
                cur.execute("""INSERT INTO users (fname, lname, username, password, dob, email, joindate, location, bio)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (self.fname, self.lname, self.username, self.password, self.dob, self.email, self.joindate, self.location, self.bio))
                self.id = cur.lastrowid
        else:
            self.update('fname', self.fname)
            self.update('lname', self.lname)
            self.update('password', self.password)
            self.update('email', self.email)
            self.update('location', self.location)
            self.update('bio', self.bio)
        conn.commit()
        #User name and id can't change

    def delete(self):
        cur = conn.cursor()
        cur.execute('''DELETE FROM users
                    WHERE id = ?''', (self.id,))
        conn.commit()

    def get_contributed_stories(self):
        cur = conn.cursor()
        cur.execute("""SELECT s.id
            FROM stories s JOIN paragraph p ON s.id = p.story_id JOIN users u ON p.author_id = u.id
            WHERE u.id = ?""",
            (self.id,))
        rows = cur.fetchall()
        results = []
        for row in rows:
            results += dbapi.story.Story.find("id", *row)
        return results

    def get_stories(self):
        cur = conn.cursor()
        cur.execute("""SELECT s.id
            FROM stories s JOIN users u ON s.author_id = u.id
            WHERE u.id = ?""",
            (self.id,))
        rows = cur.fetchall()
        results = []
        for row in rows:
            results += dbapi.story.Story.find("id", *row)
        return results

    def get_number_of_stories(self):
        return len(self.get_stories())

    def get_number_of_paragraphs(self):
        cur = conn.cursor()
        cur.execute("""SELECT id
            FROM paragraphs
            WHERE author_id = ?""",
            (self.id,))
        rows = cur.fetchall()
        results = []
        for row in rows:
            results += Paragraph.find("id", *row)
        return len(results)

    def get_number_of_paragraphs_approved(self):
        cur = conn.cursor()
        cur.execute("""SELECT id
            FROM paragraphs
            WHERE author_id = ? AND approved = 1""",
            (self.id,))
        rows = cur.fetchall()
        results = []
        for row in rows:
            results += Paragraph.find("id", *row)
        return len(results)
    

if __name__ == "__main__":
    s = User.find('username', 'barry_1233')[0]
    previous_name = s.fname
    if s.fname == "Barry":
        s.fname = "Melissa"
    else:
        s.fname = "Barry"
    s.save()
    s2 = User.find('username', 'barry_1233')[0]
    assert s2.fname != previous_name, "Name didn't change :("        

    stories = s2.get_stories()
    assert len(stories), "Should have some stories"


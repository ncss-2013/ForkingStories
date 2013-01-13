import __importfix__; __package__ = 'dbapi'

from .__init__ import *
from dbapi.user import *
import dbapi.dbtime as dbtime

import sqlite3

class Comment(object):
    '''


    '''

    def __init__(self, comment_id:int,author_id:int,story_id:int,content:str,created_time:str):
        self.id = comment_id
        self.author_id = author_id
        self.story_id = story_id
        self.content = content
        self.created_time = created_time

    def save(self):
        cur = conn.cursor()
        if self.id == None:
            time = dbtime.make_time_str()
            self.created_time = dbtime.get_time_from_str(time)
            cur.execute("INSERT INTO comments VALUES (NULL, ?, ?, ?, ?, ?);",
                        (self.author_id,self.story_id,self.content,self.created_time))
            self.id = cur.lastrowid
        else:
            cur.execute('''UPDATE comments SET
                    author_id=?,
                    story_id=?,
                    content=?,
                    WHERE id=?'''(self.author_id,self.story_id,self.content,self.id))
        conn.commit()

    def delete(self):
        if self.id is not None:
            cur = conn.cursor()
            cur.execute("DELETE FROM comments WHERE id = ?",(self.id,))
            self.id = None
            conn.commit()

    def get_author(self):
        cur = conn.cursor()
        return User.find('id', self.author_id)

    @classmethod
    def create(cls, userObj:object, storyObj:object, content:str):
        return Comment(None, userObj.id, storyObj, content, None)
    

    
        
        

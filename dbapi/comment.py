import __importfix__; __package__ = 'dbapi'

from .__init__ import *
import dbapi.user
import dbapi.dbtime as dbtime

import sqlite3

class Comment(object):
    '''
        Comment class for database interfacing
        
            --- Written by Nicholas Verstegen ---
        save() --> saves comment object to database
        
        delete() --> removes the comment object from the database
        
        find(field_name,field_value) --> returns a list of comment objects
                               Valid field_names: 'id', 'created_time',
                                           'content', 'author', 'all',
                                           'story_id'

        get_author() --> returns author object for the comment in a list

        .content --> is the content string of the comment
        .created_time --> a time object from the time of first save to database
        
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
            cur.execute("INSERT INTO comments VALUES (NULL, ?, ?, ?, ?);",
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
        try:
            return dbapi.user.User.find('id', self.author_id)[0]
        except IndexError:
            return None

    @classmethod
    def create(cls, userObj:object, storyObj:object, content:str):
        return Comment(None, userObj.id, storyObj.id, content, None)

    @classmethod
    def find(cls, field_name, field_value):
        if field_name == 'author':
            field_name = 'author_id'
            field_value = field_value.id
        cur = conn.cursor()
        if field_name == 'all':
            cur.execute("SELECT * FROM comments")
        else:
            cur.execute("SELECT * FROM comments WHERE " + field_name + "= ?",(field_value,))
        records = cur.fetchall()
        comments = []
        for record in records:
            comment = Comment(*record)
            comment.created_time = dbtime.get_time_from_str(record[4])
            comments.append(comment)
        return comments

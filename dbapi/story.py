import __importfix__; __package__ = 'dbapi'

from .__init__ import *
from dbapi.paragraph import Paragraph as Paragraph
import dbapi.dbtime as dbtime

import sqlite3

class RecordNotFound(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class Story(object):
    '''
        Story class for database interfacing.
        
            --- Written by Nicholas Verstegen ---
        save() --> saves story object to database
        delete() --> removes the story object from the database
        get_paragraphs() --> returns a list of paragraphs
                                that belong to the story

        get(field_name,field_value) --> returns a list of story objects
                               Valid field_names: 'id', 'created_time',
                                           'title', 'author_id', 'all'
                                Raises RecordNotFound if no records
        create(author_id, title) --> returns a new story object

    '''
    def __init__(self, story_id:int,author_id:int,title:str,created_time:float):
        self.id = story_id
        self.author_id = author_id
        self.title = title

    def save(self):
        cur = conn.cursor()
        if self.id is None:
            self.created_time = dbtime.make_time_float()
            cur.execute("INSERT INTO stories VALUES (NULL, ?, ?, ?);",
                        (self.author_id,self.title,self.created_time))
            #TODO: get db id and add to object
            self.id = cur.lastrowid
        else:
            cur.execute('''UPDATE stories SET
                        author_id=?,
                        title=?,
                        WHERE id=?'''(self.author_id,self.title,self.id))
        conn.commit()
        print('saved')

    def delete(self):
        if self.id is not None:
            cur = conn.cursor()
            cur.execute("DELETE FROM stories WHERE id = ?",(self.id,))
            self.id = None
            conn.commit()

    def get_paragraphs(self):
        cur = conn.cursor()
        return Paragraph.get('story_id', self.id)
    
    @classmethod
    def find(cls, field_name, field_value):
        cur = conn.cursor()
        if field_name == 'all':
            cur.execute("SELECT * FROM stories")
        else:
            print("Searching for", field_name, field_value)
            cur.execute("SELECT * FROM stories WHERE " + field_name + "= ?",(field_value,))
        records = cur.fetchall()
        stories = []
        for record in records:
            stories.append(Story(*record))
        return stories
                    
    @classmethod
    def create(cls, author_id:int, title:str):
        return Story(None, author_id, title, None)

if __name__ == "__main__":
    story = Story.create(12,'hello')
    story.save()
    stories = Story.find('author_id',12)
    assert len(stories) > 0, 'stroies should have at leats 1 story'
    count = len(stories)
    stories[0].get_paragraphs()

    story.delete()
    story.find('author_id',12)
    stories = Story.find('author_id',12)
    assert len(stories) < count, 'should now have fewer stories'

        
        

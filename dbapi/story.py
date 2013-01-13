import __importfix__; __package__ = 'dbapi'

from .__init__ import *
from dbapi.paragraph import Paragraph as Paragraph
from dbapi.user import *
import dbapi.dbtime as dbtime

import sqlite3


class Story(object):
    '''
        Story class for database interfacing.
        
            --- Written by Nicholas Verstegen ---
        save() --> saves story object to database
        delete() --> removes the story object from the database
        get_paragraphs() --> returns a list of paragraphs
                                that belong to the story
        get_author() --> returns author object in a list that
                            made the story

        find(field_name,field_value) --> returns a list of story objects
                               Valid field_names: 'id', 'created_time',
                                           'title', 'author_id',
                                           'author_init_comment', 'all'
        create(author_id, title, author_init_comment) --> returns a new story object,
                                                        author_init_comment is optional and
                                                        defults to an empty string
        get_accepted_paragraphs() --> returns paragraph objects that are acccepted
                                        by having required number of votes

    '''
    def __init__(self, story_id:int,author_id:int,title:str,created_time:str,author_init_comment:str):
        self.id = story_id
        self.author_id = author_id
        self.title = title
        self.author_init_comment = author_init_comment

    def save(self):
        cur = conn.cursor()
        if self.id is None:
            time = dbtime.make_time_str()
            self.created_time = dbtime.get_time_from_str(time)
            cur.execute("INSERT INTO stories VALUES (NULL, ?, ?, ?, ?);",
                        (self.author_id,self.title,time,self.author_init_comment))
            self.id = cur.lastrowid
        else:
            cur.execute('''UPDATE stories SET
                        author_id=?,
                        title=?,
                        WHERE id=?'''(self.author_id,self.title,self.id))
        conn.commit()

    def delete(self):
        if self.id is not None:
            cur = conn.cursor()
            cur.execute("DELETE FROM stories WHERE id = ?",(self.id,))
            self.id = None
            conn.commit()

    def get_approved_paragraphs(self):
        return Paragraph.get_approved_paragraphs(self.id)

    def get_author(self):
        cur = conn.cursor()
        return User.find('id', self.author_id)

    def add_paragraph(self, paragraph):
        user_id = paragraph.author_id
        # --- Alex Mueller wrote this ---
        paragraphs = Paragraph.find('story_id', self.id)
        paragraph.parent_id = max(
            [p.parent_id for p in paragraphs if p.approved])
        paragraph.save()
        # --- End the part that Alex Mueller wrote ---
    
    @classmethod
    def find(cls, field_name, field_value):
        cur = conn.cursor()
        if field_name == 'all':
            cur.execute("SELECT * FROM stories")
        else:
            cur.execute("SELECT * FROM stories WHERE " + field_name + "= ?",(field_value,))
        records = cur.fetchall()
        stories = []
        for record in records:
            story = Story(*record)
            story.created_time = dbtime.get_time_from_str(record[3])
            stories.append(story)
        return stories
                    
    @classmethod
    def create(cls, author_id:int, title:str, author_init_comment:str=''):
        return Story(None, author_id, title, None, author_init_comment)

if __name__ == "__main__":
    story = Story.create(12,'hello')
    story.save()
    stories = Story.find('author_id',12)
    author = story.get_author()
    assert len(stories) > 0, 'stroies should have at least 1 story'
    count = len(stories)
    stories[0].get_approved_paragraphs()
    story.delete()
    story.find('author_id',12)
    stories = Story.find('author_id',12)
    assert len(stories) < count, 'should now have fewer stories'

        
        

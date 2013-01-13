#!/usr/bin/env python3
"""Story package"""
import __importfix__; __package__ = 'dbapi'

from .__init__ import *
from dbapi.paragraph import Paragraph as Paragraph
import dbapi.user
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
        get_author() --> returns author object that made the story

        find(field_name,field_value) --> returns a list of story objects
                               Valid field_names: 'id', 'created_time',
                                           'title', 'author_id', 'all'
        create(author_id, title) --> returns a new story object

    '''
    def __init__(self, story_id:int,author_id:int,title:str,created_time:float):
        self.id = story_id
        self.author_id = author_id
        self.title = title

    def save(self):
        cur = conn.cursor()
        if self.id is None:
            time = dbtime.make_time_float()
            self.created_time = dbtime.create_datetime(time)
            cur.execute("INSERT INTO stories VALUES (NULL, ?, ?, ?);",
                        (self.author_id,self.title,time))
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

    def get_paragraphs(self):
        # TODO: Integrate with Paragraph stuff.
        return Paragraph.get_approved_content(self.id)

    def get_author(self):
        # TODO: Integrate with User stuff.
        cur = conn.cursor()
        return dbapi.user.User.find('id', self.author_id)
    
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
            story.created_time = dbtime.create_datetime(record[3])
            stories.append(story)
        return stories
                    
    @classmethod
    def create(cls, author_id:int, title:str):
        return Story(None, author_id, title, None)

if __name__ == "__main__":
    story = Story.create(12,'hello')
    story.save()
    stories = Story.find('author_id',12)
    author = story.get_author()
    assert len(stories) > 0, 'stories should have at least 1 story'
    count = len(stories)
    stories[0].get_paragraphs()
    story.delete()
    story.find('author_id',12)
    stories = Story.find('author_id',12)
    assert len(stories) < count, 'should now have fewer stories'

        
        

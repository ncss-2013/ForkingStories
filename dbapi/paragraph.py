#!/usr/bin/env python3
'''paragraph.py

Contains a Paragraph object to interface with the paragraph table in the
database.

Written by Alex Mueller and Waseem Sajeev

'''

import __importfix__; __package__ = 'dbapi'

from .__init__ import *
import dbapi.dbtime as dbtime



class Paragraph(object):
    '''This class represents a row in the paragraph table.

Use Paragraph.get(<some query>, <fieldname for query>) to fetch a list
of Paragraph objects representing rows in the paragraph table.

Use p = Paragraph(<values>) to create a new row in memory, where <values>
representes all of the table values in the order that they appear in the
actual table not including 'created' and 'id'.

Use p.save() to add the paragraph row to the database, where p is
an instantiated Paragraph object.

'''
    def __init__(self, para_id:int, content:str, parent_id:int,
                 votes:int, author_id:int, approved:int, story_id:int,
                 created_time:float):
        self.id = para_id
        self.content = content
        self.parent_id = parent_id
        self.votes = votes
        self.created_time = created_time
        self.author_id = author_id
        self.approved = approved
        self.story_id = story_id

    def save(self):
        cur = conn.cursor()
        if not self.id:
            now = dbtime.make_time_float()
            cur.execute(
                'INSERT INTO paragraphs VALUES'
                '(NULL, ?, ?, ?, ?, ?, ?, ?);',
                (self.content, self.parent_id, self.votes,
                 now, self.author_id, self.approved,
                 self.story_id))
            self.id = cur.lastrowid
            self.created = now
        else:
            cur.execute(
                '''UPDATE paragraphs 
SET content = ?,
parent_id = ?,
votes = ?,
author_id = ?,
approved = ?,
story_id = ?
WHERE id = ?''', (self.content, self.parent_id, self.votes,
                  self.author_id, self.approved, self.story_id,
                  self.id))
        # Commit data
        conn.commit()

    def delete(self):
        cur = conn.cursor()
        cur.execute('DELETE FROM paragraphs WHERE id = ' + str(
            self.id) + ';')
        conn.commit()

    def get_author(self):
        from dbapi.user import User
        try:
            return User.find('id', self.author_id)[0]
        except IndexError:
            raise Exception('This paragraph has no exsiting author'
                            ' in the datebase.')

    def get_story(self):
        from dbapi.story import Story
        try:
            return Story.find('id', self.story_id)[0]
        except IndexError:
            raise Exception('This paragraph does not belong to any exsiting'
                            ' story in the datebase.')

    @classmethod
    def create (clf, content:str, parent_id:int, votes:int,
                 author_id:int, approved:bool, story_id:int):
        return Paragraph(None, content, parent_id, votes, author_id,
                         1 if approved else 0,
                         story_id, -1)
        


    @classmethod
    def find(clf, field_name, query, order_by=None):
        cur = conn.cursor()
        if not order_by:
            order_by = field_name
            
        # TODO: This is a bug, maybe escape field_name later
        rows = cur.execute('SELECT * FROM paragraphs WHERE ' + field_name + ' = ?'
                           'ORDER BY ?',
                        (query, order_by)).fetchall()
        return [Paragraph(p[0], p[1], p[2], p[3], p[4], p[5], p[6],
                         dbtime.create_datetime(p[7])) for p in rows]

    @classmethod
    def get_approved_paragraphs(clf, story_id):
        # TODO: Update docstrings
        '''Takes a story id and returns a list of all the aprroved content
in order for that story.'''
        cur = conn.cursor()
        cur.execute('''SELECT * FROM paragraphs WHERE
story_id = ''' + str(story_id) + ''' AND approved = 1
ORDER BY parent_id;''')
        rows = cur.fetchall()
        return [Paragraph(p[0], p[1], p[2], p[3], p[4], p[5], p[6],
                         dbtime.create_datetime(p[7])) for p in rows]
            
        

if __name__ == '__main__':
    p = Paragraph.create('It\'s a cave troll! Save the hobbits! Aragorn!',
                  1, 10, 0,
                  False, 0)
    p.save()

    q = Paragraph.find('id', p.id, 'story_id')
    assert len(q) > 0, 'Some paragraph should exsist.'
    print(q[0].content)
    print('Author:', p.get_author())
    print('Story:', p.get_story())
    p.delete()
            
            

#!/usr/bin/env python3
'''paragraph.py

Contains a Paragraph object to interface with the paragraph table in the
database.

Written by Alex Mueller and Waseem Sajeev

'''

from __init__ import *
import dbtime

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
    def __init__(self, content:str, parent_id:int or None, votes:int,
                 author_id:int, approved:bool, story_id:int,
                 _created=None, _id=None):
        self.id = _id
        self.content = content
        self.parent_id = parent_id
        self.votes = votes
        self.created = _created
        self.author_id = author_id
        self.approved = 1 if approved else 0
        self.story_id = story_id

    def save(self):
        cur = conn.cursor()
        if not self.id:
            cur.execute(
                'INSERT INTO paragraph VALUES'
                '(NULL, ?, ?, ?, ?, ?, ?, ?);',
                (self.content, self.parent_id, self.votes,
                 dbtime.make_time_str(), self.author_id, self.approved,
                 self.story_id))
        else:
            cur.execute(
                '''UPDATE paragraph 
SET content = ?,
parent_id = ?,
votes = ?,
author_id = ?,
approved = ?,
story_id = ?
WHERE id = ?''', (self.content, self.parent_id, self.votes,
                  self.author_id, self.approved, self.story_id,
                  self.id))


    @classmethod
    def get(self, field_name, query):
        cur = conn.cursor()
        # TODO: This is a bug, maybe escape field_name later
        rows = cur.execute('SELECT * FROM paragraph WHERE ' + field_name + ' = ?'
                           'ORDER BY ?',
                        (query, field_name)).fetchall()
        return [Paragraph(p[1], p[2], p[3], p[4], p[5], p[6],
                         _created=dbtime.get_time_from_str(p[7]),
                         _id=p[0]) for p in rows]
        

if __name__ == '__main__':
    p = Paragraph('It\'s a cave troll! Save the hobbits! Aragorn!',
                  1, 10, 0,
                  False, 0);
    p.save()

    q = Paragraph.get('id', 1)
    assert len(q) > 0, 'Some paragraph should exsist.'
    print(q[0].content)
            
            

#!/usr/bin/env python3
'''paragraph.py

Contains a Paragraph object to interface with the paragraph table in the
database.

Written by Alex Mueller and Waseem Sajeev

'''

from .__init__ import conn

class Paragraph(object):
    def __init__(self, para_id:int, content:str, parent_id:int, votes:int, \
                 created:str, author_id:int, approved:bool, story_id:int):
        #TODO: Make id = None
        self.id = para_id
        self.content = content
        self.parent_id = parent_id
        self.votes = votes
        self.created = created
        self.author_id = author_id
        self.approved = 1 if approved else 0
        self.story_id = story_id

    def save(self):
        #TODO: save vs. update
        cur = conn.cursor()
        cur.execute('INSERT INTO paragraph VALUES (?, ?, ?, ?, ?, ?, ?, ?);', (
                    self.id, self.content, self.parent_id, self.votes, 
                    self.created, self.author_id, self.approved, self.story_id))

    @classmethod
    def get_by_id(self, para_id):
        cur = conn.cursor()
        p = cur.execute('SELECT * FROM paragraph WHERE id = ?;', (para_id,)).fetchone()
        if p:
            return Paragraph(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7])
        

if __name__ == '__main__':
    p = Paragraph(1, "It is a truth universally acknowledged, ", 0, 99, "DD-MM", 2, True, 5)
    p.save()

    q = Paragraph.get_by_id(1)
    print(q.content)
            
            

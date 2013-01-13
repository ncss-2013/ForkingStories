import __importfix__; __package__ = 'dbapi'

from .__init__ import *
from dbapi.paragraph import Paragraph as Paragraph
from dbapi.user import *
from dbapi.comment import *
import dbapi.dbtime as dbtime
from dbapi.rules import *

import sqlite3


class Story(object):
    '''
        Story class for database interfacing
        
            --- Written by Nicholas Verstegen ---
        save() --> saves story object to database
        
        delete() --> removes the story object from the database
        
        get_paragraphs() --> returns a list of paragraphs
                                that belong to the story
                                
        get_author() --> returns author object in a list that
                            made the story

        find(field_name,field_value) --> returns a list of story objects
                               Valid field_names: 'id', 'created_time',
                                           'title', 'author',
                                           'author_init_comment', 'all', 'votes'

        create(author_obj, title, author_init_comment) --> returns a new story object,
                                                        author_init_comment is optional and
                                                        defults to an empty string

        get_accepted_paragraphs() --> returns paragraph objects of the story

        add_paragraph(userObj, content, parent_id) --> returns a new paragraph object for the story

        get_comments() --> returns a list of comment objects for the story

        up_vote() --> increments the votes for the story

        set_rule(rule_def_name, parameter) --> gives the story a rule of type specified
                                                with the parameter
                                                Valid rule_def_names; 'letters_per_word',
                                                'banned_words', 'max_num_words', 'forced_words',
                                                'include_number_words'

        .created_time --> a time object from the time of first save to database
        .votes --> votes of the object
        
    '''
    def __init__(self, story_id:int,author_id:int,title:str,created_time:str,author_init_comment:str, votes:int):
        self.id = story_id
        self.author_id = author_id
        self.title = title
        self.author_init_comment = author_init_comment
        self.votes = votes
        self.created_time = created_time

    def save(self):
        cur = conn.cursor()
        if self.id is None:
            time = dbtime.make_time_str()
            self.created_time = dbtime.get_time_from_str(time)
            cur.execute("INSERT INTO stories VALUES (NULL, ?, ?, ?, ?, ?);",
                        (self.author_id,self.title,time,self.author_init_comment, self.votes))
            self.id = cur.lastrowid
        else:
            cur.execute('''UPDATE stories SET
                        author_id=?,
                        title=?,
                        WHERE id=?'''(self.author_id,self.title,self.id))
        conn.commit()
        return self

    def delete(self):
        if self.id is not None:
            cur = conn.cursor()
            cur.execute("DELETE FROM stories WHERE id = ?",(self.id,))
            self.id = None
            conn.commit()
            cur.execute("DELETE FROM rules WHERE story_id = ?",(self.id,))

    def get_approved_paragraphs(self):
        return Paragraph.get_approved_paragraphs(self.id)

    def get_comments(self):
        return Comment.find('story_id', self.id)

    def up_vote():
        self.votes += 1

    def get_author(self):
        cur = conn.cursor()
        return User.find('id', self.author_id)

    def add_paragraph(self, userObj:object, content:str, parent_id=None):
        '''This method should be used to create the first paragraph in a
story. After that, use the Paragraph.chain_paragraph() method.'''
        # --- Alex Mueller wrote this ---
        paragraph = Paragraph.create(content, None, 1, userObj.id, True,
                                     self.id)
        #paragraphs = Paragraph.find('story_id', self.id)
        #parent_ids = [p.parent_id for p in paragraphs if p.approved]
        paragraph.parent_id = parent_id if parent_id else -1
        return paragraph
        # --- End the part that Alex Mueller wrote ---

    def add_comment(self, userObj:object, content:str):
        return Comment.create(userObj, self, content)

    def set_rule(self, rule_def_name:str, params:str):
        Rules.add_rule(self.id, rule_def_name, params)

    def check_rules(self, content:str):
        return Rules.check(content, self.id)
        
    @classmethod
    def find(cls, field_name, field_value):
        if field_name == 'author':
            field_name = 'author_id'
            field_value = field_value.id
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
    def create(cls, author_obj:object, title:str, author_init_comment:str=''):
        author_id = author_obj.id
        return Story(None, author_id, title, None, author_init_comment, 0)

if __name__ == "__main__":
    user=User.find('username','barry_1233')
    story = Story.create(user[0],'hello')
    story.save()
    p = story.add_paragraph(user[0], 'Hey! Where\'s my hobbit?')
    assert p.content == 'Hey! Where\'s my hobbit?'
    p.save()
    story.get_approved_paragraphs()
    assert Paragraph.find('id', p.id)[0].content == 'Hey! Where\'s my hobbit?', \
        'Failed to read content back from databse when testing Story.create()'
    p.delete()
    stories = Story.find('author',user[0])
    author = story.get_author()
    assert len(stories) > 0, 'stroies should have at least 1 story'
    count = len(stories)
    stories[0].get_approved_paragraphs()
    comment=story.add_comment(user[0],'That was a cool read!')
    comment.save()
    story.get_comments()
    comment.delete()
    story.set_rule('banned_words','cat')
    assert False == story.check_rules('the cat sat on the mat')
    story.delete()
    story.find('author_id',12)
    stories = Story.find('author_id',12)
    assert len(stories) < count, 'should now have fewer stories'
    

        
        

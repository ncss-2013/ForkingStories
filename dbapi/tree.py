#!/usr/bin/env python
'''Has functions which can be used to create a tree of Paragraph objects.'''

import __importfix__; __package__ = 'dbapi'
from .__init__ import *

class Node(object):
    def __init__(self, paragraph):
        self.paragraph = paragraph
        self.parent = None
        self.children = []

    def add_child(self, paragraph):
        self.children.append(paragraph)

def create_tree(story):
    from dbapi.paragraph import Paragraph
    paragraphs = Paragraph.get_approved_paragraphs(story.id)
    tree = dict()
    for p in paragraphs:
        tree[p.id] = Node(p)
    for p in paragraphs:
        parent = tree[p.parent_id] if p.parent_id != -1 else None
        tree[p.id].parent = \
            parent if p.parent_id != -1 else None
        if p.parent_id != -1:
            tree[p.parent_id].children.append(tree[p.id])
    return tree[0]

if __name__ == '__main__':
    from dbapi.story import Story
    

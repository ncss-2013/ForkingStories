#!/usr/bin/env python
'''Has functions which can be used to create a tree of Paragraph objects.

Written by Alex Mueller with a lot of direction from James

'''

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
    # NOTE TO JAMES: There are probably 10 times more efficent and more
    # pythonic ways to write this functions. Please point them out to me
    # if any come to mind. I am eager to become a better programmer!
    from dbapi.paragraph import Paragraph
    paragraphs = Paragraph.get_approved_paragraphs(story.id)
    tree = dict()
    
    # Create dict of nodes
    
    for p in paragraphs:
        tree[p.id] = Node(p)
        
    # Fill out the node data
    
    for p in paragraphs:
        parent = tree[p.parent_id] if p.parent_id != -1 else None
        tree[p.id].parent = \
            parent if p.parent_id != -1 else None
        if p.parent_id != -1:
            tree[p.parent_id].children.append(tree[p.id])
    # Find and return the root node
    
    # Get the node that is probably closet to the root of the dictionary
    a_node = tree[next(tree.values()).paragraph.id]
    # Loop up the tree to the root node
    while a_node.parent != -1:
        a_node = a_node.parent
    return a_node
    

if __name__ == '__main__':
    pass
    #from dbapi.story import Story
    #print(create_tree(Story.find('id', 0)[0]))
    

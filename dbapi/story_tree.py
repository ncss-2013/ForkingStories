#!/usr/bin/env python
'''
Creates a tree of the Paragraph objects of a story in the database.
Written by Alex Mueller
'''

import __importfix__; __package__ = 'dbapi'
from .__init__ import *

class ParagraphNode(object):
	def __init__(self, paragraph):
		self.paragraph = paragraph
		self.parent = None
		self.children = []

	def add_child(self, paragraph):
		self.children.append(paragraph)

def create_tree(story=None,story_id=None):
	if story_id is None:
		story_id = story.id
	from dbapi.paragraph import Paragraph
	paragraphs = Paragraph.get_approved_paragraphs(story_id)
	tree = dict((p.id, ParagraphNode(p)) for p in paragraphs)
		
	# Fill out the node data
	root = None
	for p in paragraphs:
		if p.parent_id != -1:
			tree[p.id].parent = tree[p.parent_id]
			tree[p.parent_id].children.append(tree[p.id])
		else:
			root = tree[p.id]
	
	# Return the root node
	return root


if __name__ == '__main__':
	pass
	#from dbapi.story import Story
	#print(create_tree(Story.find('id', 0)[0]))
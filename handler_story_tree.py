import template
from dbapi.story_tree import create_tree
from dbapi.story import Story
from dbapi.user import User
from dbapi.paragraph import Paragraph
from dbapi.rules import Rules

'''
def add_static_story():
	barry = User.find('id', '0')[0]
	story = Story.create(barry, 'ITS A STORY', 'No comment.')
	story.save()
	para = story.add_paragraph(barry, 'BLAH').save()
	para2 = para.chain_paragraph(barry, 'IM A CHILD PARAGRAPH').save()
	para3 = para.chain_paragraph(barry, 'ANOTHER CHILD PARA').save()
	para4 = para3.chain_paragraph(barry, 'AWESOME').save()
	para5 = para4.chain_paragraph(barry, 'TEH RECURSION').save()
	para6 = para4.chain_paragraph(barry, 'IS SAH').save()
	para7 = para4.chain_paragraph(barry, 'AWESUM').save()
'''

def display_story_tree(resp, story_id):
	user = resp.get_secure_cookie('username')
	story = Story.find('id', story_id)[0]
	author = User.find('id', story.author_id)[0]
	if user is not None:
		user = User.find('username', str(user, 'utf-8'))[0]
	else:
		user = None
	try:
		resp.write(template.render_file('view_story_tree.html', {'node': create_tree(story), 'story': story, 'author': author, 'user': user}))
	except Exception as e:
		story.delete()


def add_to_story_tree(response, story_id):
	try:
		story_id = int(story_id)

		username = response.get_secure_cookie('username')
		user = User.find('username', str(username,'utf-8'))[0]
		addition_to_story = response.get_argument('paragraph')
		story = Story.find('id', story_id)[0]

		if False:#not Rules.check(addition_to_story, story.id):
			#return to story view without updating.... TODO: show error
			response.write('DR')
			response.redirect('/view_story/{}'.format(story_id))
			return

		response.write('aoeuhotnaeuhaoe ')
		parent = Paragraph.find('id',int(response.get_argument('parentId')))[0]
		
		if parent:
			parent.chain_paragraph(user, addition_to_story).save()

		response.redirect('/view_story/{}'.format(story_id))
	
	except Exception as e:
		response.write(str(e))
		raise e
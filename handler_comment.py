import template
from dbapi.user import User
from dbapi.story import Story

def add_comment(response, story_id):
    username = response.get_secure_cookie('username')
    user = User.find('username', str(username, 'utf-8'))
    if not user:
        raise Exception("Expected user account when adding to story")
    user = user[0]
    story = Story.find('id', story_id)[0]
    story.add_comment(user, response.get_argument('commentbox')).save()
    response.redirect('/view_story/{}'.format(story_id))
    

import template
from dbapi.user import User
from dbapi.story import Story

def view_story(response, id):
    user = response.get_secure_cookie('username')
    story = Story.find('id', id)
    author = User.find('id', story[0].author_id)

    if user is not None:
        context = {'current_user':User.find('username', str(user, 'utf-8'))[0], 'story':story[0], 'author':author[0]}
    else:
        context = {'current_user':None, 'story':story[0], 'author':author[0]}

    html = template.render_file('templates/viewingstory.html', context)
    response.write(html)

def view_story_list(response):
    user = response.get_secure_cookie('username')

    stories = Story.find('all', '')

    if user is not None:
        context = {'current_user':User.find('username', str(user, 'utf-8'))[0], 'stories':stories}
    else:
        context = {'current_user':None, 'stories':stories}

    html = template.render_file('templates/storylist.html', context)
    response.write(html)

def add_to_story(response, id):
    username = response.get_secure_cookie('username')
    user = User.find('username',  str(username, 'utf-8'))

    if not user:
        raise Exception("Expected user account when adding to story")
    user = user[0]

    addition_to_story = response.get_argument('paragraph')
    story = Story.find('id', id)[0]

    added_paragraph = story.add_paragraph(user, addition_to_story)
    added_paragraph.save()

    response.redirect('/view_story/{}'.format(id))

    #html = template.render_file('templates/viewingstory.html', context)
    #response.write(html)

def process_new_story(response):
    username = response.get_secure_cookie('username')
    user = User.find('username', str(username, 'utf-8'))[0]

    title = response.get_argument('title')
    story = response.get_argument('story')
    rule = response.get_argument('rule')
    comment = response.get_argument('comment')

    story = Story.create(user, title, story)
    story.save()
    response.redirect('/view_story/{}'.format(story.id))

def new_story(response):
    user = response.get_secure_cookie('username')
    if user is not None:
        context = {'current_user':User.find('username', str(user, 'utf-8'))[0]}
    else:
        context = {'current_user':None}

    html = template.render_file('templates/newstory.html', context)
    response.write(html)

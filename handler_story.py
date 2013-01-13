import template
from dbapi.user import User

def view_story(response):
    user = response.get_secure_cookie('username')
    if user is not None:
        context = {'current_user':User.find('username', str(user, 'utf-8'))[0]}
    else:
        context = {'current_user':None}

    html = template.render_file('templates/viewingstory.html', context)
    response.write(html)

def view_story_list(response):
    user = response.get_secure_cookie('username')
    if user is not None:
        context = {'current_user':User.find('username', str(user, 'utf-8'))[0]}
    else:
        context = {'current_user':None}

    html = template.render_file('templates/storylist.html', context)
    response.write(html)

def add_to_stories(response):
    user = response.get_secure_cookie('username')
    if user is not None:
        context = {'current_user':User.find('username', str(user, 'utf-8'))[0]}
    else:
        context = {'current_user':None}

    html = template.render_file('templates/addingtostory.html', context)
    response.write(html)

def new_story(response):
    user = response.get_secure_cookie('username')
    if user is not None:
        context = {'current_user':User.find('username', str(user, 'utf-8'))[0]}
    else:
        context = {'current_user':None}

    html = template.render_file('templates/newstory.html', context)
    response.write(html)
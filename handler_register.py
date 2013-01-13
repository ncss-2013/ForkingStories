import sqlite3
import re
import template
from dbapi.user import User

def register(response):
    if response.get_secure_cookie('username') is not None:
        current_user = User.find('username', str(response.get_secure_cookie('username'), 'utf-8'))[0]
    else:
        current_user = None

    context = {
        'current_user':current_user
    }

    html = template.render_file('templates/registration.html', context)
    response.write(html)

def process_register(response):
    # Username should be 4 or more characters of only numbers and letters
    username_pat = re.compile(r'[a-zA-Z0-9]{4}[a-zA-Z0-9]*')
    
    firstname = response.get_argument('fname', default='')
    lastname = response.get_argument('lname', default='')
    username = response.get_argument('username')
    password = response.get_argument('password')
    repeat_password = response.get_argument('rpassword')
    email = response.get_argument('email')
    birthdate = response.get_argument('bday', default='')
    location = response.get_argument('location', default='')
    bio = response.get_argument('bio', default='')

    if username_pat.match(username) and password == repeat_password:
        user = User.create(firstname, lastname, username, password, birthdate, email, location, bio)
        user.save()
        
        response.set_secure_cookie('username', username)
        response.redirect('/user/{}'.format(username))
    else:
        response.write('Please check the username entered meets criteria and both passwords match.')

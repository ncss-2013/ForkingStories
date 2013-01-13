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
    
    firstname = response.get_argument('fname')
    lastname = response.get_argument('lname')
    username = response.get_argument('username')
    password = response.get_argument('password')
    repeat_password = response.get_argument('rpassword')
    email = response.get_argument('email')
    birthyear = response.get_argument('birthyear')
    birthmonth = response.get_argument('birthmonth')
    birthday = response.get_argument('birthday')
    location = response.get_argument('location')
    bio = response.get_argument('bio')

    #user_exists = User.get(username)
    user_exists = False

    # Check username fits criteria (regex) and password matches the repeated password
    if username_pat.match(username) and password == repeat_password and not user_exists:
        user = User.create(firstname, lastname, username, password, int(birthyear), int(birthmonth), int(birthday), email, location, bio, None)
        user.save()

        response.redirect('/')
    else:
        response.write('Please check the username entered meets criteria and both passwords match.')
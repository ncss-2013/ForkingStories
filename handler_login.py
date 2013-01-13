import template
from dbapi.user import User


def check_login(username, password):
    return User.login(username, password)

def login(response):
    response.write('''
        <!doctype html>
        <html>
            <head>
            </head>
            <body>
                <h1>Hello!</h1>
                <form action='/authenticate' method="POST">
                    <label>Username:
                        <input type='text' name='username'>
                    </label>
                    <p><label>Password:
                        <input type='password' name='password'>
                    </label>
                    <p><input type='submit' value='login'>
                </form>
            </body>
        </html>''')


def authenticate(response):
    username = response.get_field('username')
    password = response.get_field('password')
    try:
        check_login(username, password)
    except TypeError:
        response.set_secure_cookie('error_msg', 'invalid login credentials')
        response.redirect('/')
        return

    if check_login(username, password) or response.get_secure_cookie('username'):
        response.set_secure_cookie('username', username)
        response.redirect('/user/{}'.format(username))
    else:
        response.set_secure_cookie('error_msg', 'invalid login credentials')

        response.redirect('/')


def logout(response):
    response.clear_cookie('username')
    response.redirect('/')

def changepassword(response):
    old_password = response.get_field('old_password')
    new_password_1 = response.get_field('new_password_1')
    new_password_2 = response.get_field('new_password_2')

    if old_password is None:
        response.write("<p>Old password not entered.</p>")
        return
    elif new_password_1 is None:
        response.write("<p>New password not entered.</p>")
        return
    elif new_password_2 is None:
        response.write("<p>New password repeat not entered.</p>")
        return
    
    username = str(response.get_secure_cookie('username'), 'utf-8')
    if new_password_1 == new_password_2:
        user = check_login(username, old_password)
        if user is not None:
            user.update_password(new_password_1)
            response.write('<p>Password has been changed.</p>')
        else:
            response.write('<p>Old password is incorrect.</p>')
    else:
        response.write('<p>Passwords do not match.</p>')

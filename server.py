from tornado import Server
from dbapi.user import User
import register
import user
import template

###### TODO change this to use database ######

def check_login(username,password):
    user = User.get(username)
    if user is not None and username == user.username and password == user.password:
        return user
    return None

#def change_password(username,old_password,new_password):
#    for i in users:
#        if username == i['username'] and old_password == i['password']:
#            i['password'] = new_password

#########################################

def index(response):
    username = response.get_secure_cookie('username')
    if username is not None:
        context = {'username':str(username, 'utf-8')}
    else:
        context = {'username':None}

    html = template.render_file('templates/index.html', context)
    response.write(html)

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
    if check_login(username,password) or response.get_secure_cookie('username'):
        response.set_secure_cookie('username', username)
        response.redirect('/user/{}'.format(username))

    else:
        response.write('''
            <!doctype html>
            <html>
                <head>
                </head>
                <body>
                    <p>Incorrect username or password, or username and password.</p>
                </body>
            </html>''')

def logout(response):
    response.clear_cookie('username')
    response.write('''
        <!doctype html>
        <html>
            <head>
            </head>
            <body>
                <p>Congratulations, you have successfully logged out!</p>
                <p><a href='/'>Home</a></p>
            </body>
        </html>''')

def changepassword(response):
    old_password = response.get_field('old password')
    new_password_1 = response.get_field('new password 1')
    new_password_2 = response.get_field('new password 2')
    username = str(response.get_secure_cookie('username'), 'utf-8')
    if new_password_1 == new_password_2:
        user = check_login(username, old_password)
        if user is not None:
            user.update('password', new_password_1)
            response.write('''
                <!doctype html>
                <html>
                    <head>
                    </head>
                    <body>
                        <p>Password seems to have changed.</p>
                        <p><a href='/user/{}'>Home</a></p>
                    </body>
                </html>'''.format(username))
        else:
            response.write('''
                <!doctype html>
                <html>
                    <head>
                    </head>
                    <body>
                        <p>Old password is incorrect.</p>
                        <p><form action='/changepassword'>
                            <label>Old password:
                                <input type='text' name='old password'>
                            </label>
                            <p><label>New password:
                                <input type='password' name='new password 1'>
                            </label>
                            <p><label>New password:
                                <input type='password' name='new password 2'>
                            </label>
                            <p><input type='submit' value='change password'>
                        </form>
                        <p><a href='/'>Home</a></p>
                    </body>
                </html>''')
    else:
        response.write('''
            <!doctype html>
            <html>
                <head>
                </head>
                <body>
                    <p>Passwords do not match.</p>
                    <p><form action='/changepassword'>
                        <label>Old password:
                            <input type='text' name='old password'>
                        </label>
                        <p><label>New password:
                            <input type='password' name='new password 1'>
                        </label>
                        <p><label>New password:
                            <input type='password' name='new password 2'>
                        </label>
                        <p><input type='submit' value='change password'>
                    </form>
                    <p><a href='/'>Home</a></p>
                </body>
            </html>''')

server = Server()
server.register('/', index)
server.register('/login', login)
server.register('/authenticate', authenticate)
server.register('/logout', logout)
server.register('/changepassword', changepassword)
server.register('/user/(\w[\w\d]+)', user.user)
server.register('/register', register.register)
server.register('/process_register', register.process_register)
server.run()





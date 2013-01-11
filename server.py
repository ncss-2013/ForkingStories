from tornado import Server
import profile

###### change this to use database ######

users = [
    {'id': 0, 'username': 'Night', 'name': 'Lauren', 'password': '12345'},
    {'id': 1, 'username': 'timmy', 'name': 'Tim', 'password': 'abcde'},
    {'id': 2, 'username': 'frog', 'name': 'Bob', 'password': 'vwxyz'}
    ]

def check_login(username,password):
    for i in users:
        if username == i['username'] and password == i['password']:
            return True
    return False

#def change_password(username,old_password,new_password):
#    for i in users:
#        if username == i['username'] and old_password == i['password']:
#            i['password'] = new_password

#########################################

def login(response):
    response.write('''
<!doctype html>
<html>
<head>
</head>
<body>
<h1>Hello!</h1>
<form action='/authenticate'>
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
        response.redirect('/user')

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
        if check_login(username,old_password):
            change_password(username,old_password,new_password_1)
            response.write('''
<!doctype html>
<html>
<head>
</head>
<body>
<p>Password seems to have changed.</p>
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

def user(response):
    if response.get_secure_cookie('username'):
        username = str(response.get_secure_cookie('username'), 'utf-8')
        response.write('''
<!doctype html>
<html>
<head>
</head>
<body>
<p>Greetings and salutations, {}!</p>
<p>You seem to be logged in.</p>
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
<form action='/logout'>
<input type='submit' value='logout'>
</form>
</body>
</html>'''.format(username))
    else:
        response.write('''
<!doctype html>
<html>
<head>
</head>
<body>
<p>You don't appear to be logged in...</p>
<p><a href='/'>Home</a></p>
</body>
</html>''')

server = Server()
server.register('/', login)
server.register('/authenticate', authenticate)
server.register('/logout', logout)
server.register('/changepassword', changepassword)
server.register('/user', user)
server.register('/profile/(\w[\w\d]+)', profile.profile)
server.run()





from dbapi.user import User

def profile(response, username):
	# Example user whilst waiting for DB model
	user = User.get(username)

	response.write('''
		<html>
			<head>
				<title>Profile for {} {}</title>
			</head>
			<body>
				<strong>Name: </strong> {} {}<br />
				<strong>Username: </strong> {}
			</body>
		</html>
		'''.format(user.fname, user.lname, user.fname, user.lname, user.username))

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

	#get_profile = User.get(id)

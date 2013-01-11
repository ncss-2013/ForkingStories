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

	#get_profile = User.get(id)

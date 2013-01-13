from dbapi.user import User
import template

def user(response, username):
	user = User.find('username', username)[0]

	if response.get_secure_cookie('username') is not None:
		current_user = User.find('username', str(response.get_secure_cookie('username'), 'utf-8'))[0]
	else:
		current_user = None

	context = {
	  	'user':user,
	    'current_user': current_user,
	    'requested_user': username
	}

	html = template.render_file('templates/profile.html', context)
	response.write(html)

def profiles(response):
	users = User.find('all')

	for user in users:
		response.write('<a href="/user/{}">{}</a><br />'.format(user.username, user.username))
from dbapi.user import User
import template

def user(response, username):
	user = User.get(username)

	if response.get_secure_cookie('username'):
		current_user = User.get(str(response.get_secure_cookie('username'), 'utf-8'))
	else:
		current_user = None
    
	context = {
	  	'user':user,
	    'current_user': current_user,
	    'requested_user': username
	}

	html = template.render_file('templates/user.html', context)
	response.write(html)
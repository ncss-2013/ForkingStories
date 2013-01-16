import json
import template
import tornado.web
from dbapi.user import User

def authenticated(response):
    username = response.get_secure_cookie('username')
    context = {}
    if username is not None:
        context.update({'current_user': User.find('username', str(username, 'utf-8'))[0]})
    else:
        context['current_user'] = None
    if context['current_user'] and context['current_user'].admin_level >= 1:
         return (True, context)
    else:
         return (False, context)

class EnsureAdmin(tornado.web.RequestHandler):
    def get(response, *args, **kwargs):
        is_admin, context = authenticated(response)

        if is_admin:
            context['error'] = (response.get_secure_cookie('error_msg') or b'').decode()
            response.clear_cookie('error_msg')
            response.actual_get(context, *args, **kwargs)
        else:
            response.redirect('/')

    def actual_get(self, *args, **kwargs):
        raise NotImplementedError()

class AdminIndex(EnsureAdmin):
    def actual_get(response, context, *args, **kwargs):
        context['users'] = User.find('all', '')
        html = template.render_file('templates/admin_index.html', context)
        response.write(html)


class DeleteUser(tornado.web.RequestHandler):
    def get(response, user_id):
        output = {'success': None, 'msg': None}
        is_admin, _ = authenticated(response)
        if is_admin:
            user = User.find('id', user_id)
            if user:
                output['success'] = True
                user[0].delete()
            else:
                output['success'] = False
        else:
            output['success'] = False
            output['msg'] = 'not_administrator'            
        response.write(output)






import template
import tornado.web
from dbapi.user import User


class BaseAdmin(tornado.web.RequestHandler):
    def get(response, *args, **kwargs):
        username = response.get_secure_cookie('username')
        context = {}
        if username is not None:
            context.update({'current_user': User.find('username', str(username, 'utf-8'))[0]})
        else:
            context['current_user'] = None

        if context['current_user'] and context['current_user'].admin_level >= 1:
            context['error'] = (response.get_secure_cookie('error_msg') or b'').decode()
            response.clear_cookie('error_msg')
            response.actual_get(context, *args, **kwargs)
        else:
            response.redirect('/')

    def actual_get(self, *args, **kwargs):
        raise NotImplementedError()

class AdminIndex(BaseAdmin):
    def actual_get(response, context, *args, **kwargs):
        html = template.render_file('templates/admin_index.html', context)
        response.write(html)

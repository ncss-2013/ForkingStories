import json
import logging
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
        return (True, context, context['current_user'].admin_level)
    else:
        return (False, context, 0)


class EnsureAdmin(tornado.web.RequestHandler):
    def __new__(self, *args, **kwargs):
        if not hasattr(self, '_is_setup'):
            # assert self.get != self.check_get
            # assert self.actual_get != self.get
            logging.info('Setting up')

            self.actual_get = self.get  # keep a reference to the child get
            self.get = self.check_get   # overwrite the child's get method with one that checks if the user has the required privelidges
            self._is_setup = True
        else:
            logging.info('I am setup')

        return super(EnsureAdmin, self).__new__(self)  # , *args, **kwargs)

    def check_get(response, *args, **kwargs):
        is_admin, context, admin_level = authenticated(response)

        # determine the minimum required admin level to access this page
        minimum_al = response.minimum if hasattr(response, 'minimum') else 1

        if is_admin and admin_level > minimum_al:
            context['error'] = (response.get_secure_cookie('error_msg') or b'').decode()
            response.clear_cookie('error_msg')
            # print('passg')
            response.actual_get(context, *args, **kwargs)
            # print('well')
        else:
            logging.info('Non-administrator attempting to access admin panel -> redirected to homepage')
            response.redirect('/')

    # def get(self, *args, **kwargs):
    #     self.get.original = True
    #     raise NotImplementedError()


class AdminIndex(EnsureAdmin):
    # minimum admin level required to access this page
    minimum = 1

    def get(response, context, *args, **kwargs):
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
                logging.info('Successfully deleted user with id {}'.format(user_id))
                output['success'] = True
                user[0].delete()
            else:
                logging.info('Did not successfully deleted user with id {}'.format(user_id))
                output['success'] = False
        else:
            logging.info('Non-administrator attempted to delete user {}'.format(user_id))
            output['success'] = False
            output['msg'] = 'not_administrator'
        response.write(json.dumps(output))

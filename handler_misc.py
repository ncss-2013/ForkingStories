import template


def credits(response):
    context = {'current_user': None}

    context['error'] = (response.get_secure_cookie('error_msg') or b'').decode()
    response.clear_cookie('error_msg')

    html = template.render_file('templates/credits.html', context)
    response.write(html)

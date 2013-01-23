# import logging
import template
from dbapi import conn
from dbapi.user import User
from dbapi.story import Story
from collections import defaultdict
from utils import BaseRequestHandler
from search import search, load_index
from dbapi.searchindex import create_table

create_table(conn, if_exists=False)


class SearchStories(BaseRequestHandler):
    def get(self):
        context = defaultdict()

        user = self.get_secure_cookie('username')
        stories = Story.find('all', '')

        try:
            context.update({
                'current_user': User.find('username', str(user, 'utf-8'))[0]})
        except TypeError:
            context.update({
                'current_user': None})

        cursor = conn.cursor()

        if self.get_arguments('storyquery') != []:
            query = self.get_argument('storyquery')
            results = search(cursor, conn, query)
            stories = []
            for result in results:
                stories.append(Story.find('id', int(result[0]))[0])

            context['stories'] = stories
            context['query'] = query
            context['story'] = ''

            assert 'query' in context
            print("QUERY", repr(query))
            html = template.render_file('templates/storylist.html', context)
            # html = template.render_file('templates/minimal.html', context)
            self.write(html)

        elif self.get_arguments('sort') != []:
            # filter logic here
            pass
        else:
            context['stories'] = stories
            context['story'] = None
            html = template.render_file('templates/storylist.html', context)
            self.write(html)


def debug(self):
    # query = self.get_argument('storyquery')
    query = 'gandalf'
    self.write('{}<br/>'.format(search(conn.cursor(), conn, query)))
    index = load_index(conn.cursor(), conn)
    for doc in index:
        self.write('{};<br/>'.format(doc))
        for word in index[doc]:
            self.write('<div style="margin-left:20px;">{}; {}</div>'.format(word, index[doc][word]))
        self.write('<br/>')

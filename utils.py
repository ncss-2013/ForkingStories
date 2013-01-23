#!/usr/bin/env python
import tornado.web


class BaseRequestHandler(tornado.web.RequestHandler):
    def __new__(self, *args, **kwargs):
        # self.actual_get = self.get  # keep a reference to the child get
        # self.get = self.check_get   # overwrite the child's get method with one that checks if the user has the required privelidges
        return super(BaseRequestHandler, self).__new__(self, *args, **kwargs)

    def get(self, *args, **kwargs):
        raise NotImplementedError()

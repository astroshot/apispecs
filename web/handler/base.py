# coding=utf-8
import json
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def render_json(self, data):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Content-Type', 'application/json')
        self.finish(json.dumps(
            data,
            sort_keys=True,
            indent=4))

    def get_base_url(self):
        return '{}://{}'.format(self.request.protocol, self.request.host)

# coding=utf-8
from os.path import dirname
from tornado.web import StaticFileHandler
from web.handler import HomeHandler, SpecJsonsHandler, SpecsHandler


STATICS_PATH = dirname(__file__) + '/statics'


handlers = [
    ('/', HomeHandler),
    ('/specs/([\w.-]+).json', SpecJsonsHandler),
    ('/specs/([\w.-]+)', SpecsHandler),
    ('/statics/(.*)', StaticFileHandler, {'path': STATICS_PATH}),
]

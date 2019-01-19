# coding=utf-8
from os.path import dirname
import markdown2
from tornado.web import HTTPError
from web.handler.base import BaseHandler
from web.util import LocalSchemaLoader

local_schema_loader = LocalSchemaLoader()


class HomeHandler(BaseHandler):
    def get(self):
        root_dir = dirname(dirname(dirname(__file__)))
        with open(root_dir + '/README.md') as f:
            readme_content = markdown2.markdown(f.read())
        with open(root_dir + '/CHANGELOG.md') as f:
            changes_content = markdown2.markdown(f.read())
        names = local_schema_loader.list_schema_names()
        self.render(
            'spec.html',
            base_url=self.get_base_url(),
            content={'readme': readme_content, 'changes': changes_content},
            iframe={},
            schema_names=local_schema_loader.list_schema_names())


class SpecsHandler(BaseHandler):
    def get(self, name):
        schema_names = local_schema_loader.list_schema_names()
        self.render(
            'spec.html',
            base_url=self.get_base_url(),
            content='',
            iframe={'src': ''},  # TODO: template lost
            schema_names=schema_names)


class SpecJsonsHandler(BaseHandler):
    def get(self, name):
        expand_refs = bool(self.get_argument('expand', None))
        schema = local_schema_loader.load(name, expand_refs)
        if not schema:
            raise HTTPError(404)
        self.render_json(schema)

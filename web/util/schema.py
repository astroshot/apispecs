# coding=utf-8
import os
import glob
import copy
import yaml
import jsonref

import flex
from .define import API_FILES_PATH

DEFAULT_SCHEMAS_DIR = os.path.join(os.path.abspath('.'), API_FILES_PATH)


class LocalSchemaLoader(object):
    def __init__(self, schemas_dir=DEFAULT_SCHEMAS_DIR):
        self.schemas_dir = schemas_dir

    def _get_schema_path(self, name):
        path = os.path.join(self.schemas_dir, name + '.yaml')
        if not os.path.exists(path):
            return None
        return path

    def list_schema_names(self):
        paths = glob.glob(self.schemas_dir + '/*.yaml')
        excluded_names = [
            '_metadata',
            '_parameters',
            '_definitions']
        names = [
            path.split('api_files/')[1].split('.yaml')[0]
            for path in paths]
        names = [
            n for n in names
            if n not in excluded_names]
        return sorted(names)

    def load(self, name, expand_refs=False):
        if name not in self.list_schema_names():
            return None
        with open(self.schemas_dir + '/_metadata.yaml') as f:
            metadata = yaml.load(f)
        with open(self.schemas_dir + '/_definitions.yaml') as f:
            definitions = yaml.load(f)
        with open(self.schemas_dir + '/_parameters.yaml') as f:
            parameters = yaml.load(f)
        schema_path = self._get_schema_path(name)
        with open(schema_path) as f:
            schema = yaml.load(f)
            schema = _cook_schema(schema, metadata, definitions, parameters, expand_refs)
            schema = flex.core.load_source(schema)
            return schema


class GitlabSchemaLoader(object):
    def __init__(self, token):
        pass

    def list_branch_names(self):
        pass

    def list_schema_names(self, branch_name):
        pass

    def load(self, name, branch_name):
        pass


def _cook_schema(schema, metadata, definitions, parameters, expand_refs=False):
    schema = copy.deepcopy(schema)
    schema.setdefault('info', {})
    schema['info']['version'] = metadata['API_VERSION']
    schema['definitions'] = dict(definitions, **schema.get('definitions', {}))
    schema['parameters'] = dict(parameters, **schema.get('parameters', {}))
    if expand_refs:
        schema = jsonref.JsonRef.replace_refs(schema)
    return schema


def load_schema(name):
    """load api schema
    example::

        schema = load_schema('api.example.com-coupon')
    """

    schemas_dir = DEFAULT_SCHEMAS_DIR
    if os.getenv('APISPECS_LOCAL'):
        local_schemas_dir = os.getenv('APISPECS_LOCAL')
        schemas_dir = os.path.join(local_schemas_dir, API_FILES_PATH)
    return LocalSchemaLoader(schemas_dir).load(name)

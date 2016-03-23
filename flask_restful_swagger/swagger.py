# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six
import os
import mimetypes
import importlib

from flask import Blueprint
from flask_restful import Api

from flask_restful_swagger.producers import JsonProducer, HtmlProducer
from flask_restful_swagger import swagger_definitions
from flask_restful_swagger.utils import (
    convert_from_camel_case,
)

__author__ = 'sobolevn'


class SwaggerDocs(object):
    _default_description = 'Auto generated API docs by flask-restful-swagger'
    _known_producers = [
        JsonProducer,
        HtmlProducer,
    ]

    def _import_required_version(self, version):
        """
        This method is used to dynamically import the required swagger
        api version. It loads modules based on version number from
        the `swagger_definitions` package.
        It sets `self.definitions` to the appropriate module.
        :param version: version to be loaded, eg: 1.2
        :return: None
        """
        try:
            version_name = 'v' + version.replace('.', '_')
            import_path = '{}.{}'.format(
                swagger_definitions.__name__, version_name)
            self.definitions = importlib.import_module(
                import_path
            )
        except ImportError:
            raise ValueError('No such swagger version: ' + version)

    def __init__(self,
                 api,
                 api_version='0.0',
                 swagger_version='1.2',
                 base_path='http://localhost:5000',
                 resource_path='/',
                 produces=None,
                 api_spec_url='/api/spec',
                 description=None,
                 # New kwargs since 1.0.0:
                 static_folder=None,
                 static_url_path='',
                 template_folder=None,
                 ):
        if not isinstance(api, Api):
            raise ValueError("Provided `api` object is not flask-restful's Api")

        self.api = api
        self.api_version = api_version
        self.swagger_version = swagger_version
        self.base_path = base_path
        self.resource_path = resource_path
        self.api_spec_url = api_spec_url
        self.description = description or self._default_description

        self.definitions = None
        self._import_required_version(swagger_version)

        self._detect_producers(produces)
        self.operations = []

        self.static_url_path = static_url_path
        self.static_folder = static_folder

        dir_name = os.path.dirname(__file__)
        if self.static_folder is None:
            self.static_folder = os.path.join(
                dir_name, 'static', 'swagger-ui')

        self.template_folder = template_folder
        if self.template_folder is None:
            # There's not separation between static folder and templates
            # folder, just because swagger-ui is made that way. But
            # Both of these folders are required for agile customisation.
            self.template_folder = os.path.join(
                dir_name, 'static', 'swagger-ui')

        self.app = api.app
        self.blueprint = None

        if self.app:
            # noinspection PyTypeChecker
            self.init_app(self.app)

    def init_app(self, app_or_api=None):
        try:
            self.app = app_or_api.app  # we suppose, that this is Api
        except AttributeError:
            self.app = app_or_api  # it was just app
            self.api.init_app(self.app)

        self.blueprint = Blueprint(
            self.__class__.__name__,
            self.__class__.__name__,
            url_prefix=self.api_spec_url,
            template_folder=self.template_folder,
            static_folder=self.static_folder,
            static_url_path=self.static_url_path,
        )

        for producer_class in self.produces:
            content_type = producer_class.content_type
            ext = mimetypes.guess_extension(content_type).replace('.', '')

            self.blueprint.add_url_rule(
                '/' + ext,
                view_func=self._get(ext, producer_class),
            )

        self.app.register_blueprint(self.blueprint)

    def add_resource(self, resource, *urls, **kwargs):
        return self.api.add_resource(resource, *urls, **kwargs)

    def operation(self, *args, **kwargs):
        def _inner(func):
            operation = self.definitions.SwaggerOperation(
                func, *args, **kwargs)
            self.operations.append(operation)
            return func

        return _inner

    def model(self, func):
        return func

    def _get(self, content_type, producer_class):
        def _inner():
            return producer_class(self).get()

        _inner.__name__ = content_type
        return _inner

    def _extract_specs(self):
        return {
            'apiVersion': self.api_version,
            'description': self.description,
        }

    def _detect_producers(self, produces):
        if not produces:
            self.produces = [JsonProducer]
        else:
            self.produces = []
            for producer in self.__class__._known_producers:
                for content_type in produces:
                    if producer.content_type == content_type and \
                                    producer not in self.produces:
                        self.produces.append(producer)



def docs(api, **kwargs):
    """
    This function adds endpoints for the swagger.
    It also handles all the model loading by replacing original `add_resource`
    with the patched one.

        :version changed 1.0.0
        The old docs() function before version 1.0.0 had 'camelCase' kwargs,
        which was not-PEP8, and now it is recommended to use 'snake_case'.
        But for backward compatibility 'cameCase' is also accepted.

    :param api: flask-resful's Api object
    :param kwargs: key-word arguments described in `_docs` function.
    :return: flask-resful's Api object passed as `api`.
    """
    new_kwargs = {convert_from_camel_case(k): v
                  for k, v in six.iteritems(kwargs)}
    return SwaggerDocs(api, **new_kwargs)

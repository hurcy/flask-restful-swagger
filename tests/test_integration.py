# -*- coding: utf-8 -*-

from tests.utils import BaseIntegrationTest
from tests.apps.basic_app import app

__author__ = 'sobolevn'


class TestIntegration(BaseIntegrationTest):
    app = app
    base_static_path = '/api/spec/_/static'

    def test_basic_integration(self):
        response = self.get('app/registry')
        self.assert_request_success(response)

    def test_basic_integration_json(self):
        response = self.get_raw_link('/api/spec.json')
        self.assert_request_success(response)

    def test_basic_integration_html(self):
        response = self.get_raw_link('/api/spec.html')
        self.assert_request_success(
                response, content_type='text/html; charset=utf-8')

    def test_basic_integration_resource_lister(self):
        response = self.get_raw_link('/api/spec/_/resource_list.json')
        self.assert_request_success(response)

    def test_static_integration_js(self):
        js_files = [
            'swagger-ui-bundle.js',
            'swagger-ui-standalone-preset.js',
            'swagger-initializer.js'
        ]

        for js in js_files:
            response = self.get_raw_link('{}/{}'.format(
                self.base_static_path, js))
            self.assert_request_success(
                response, content_type='application/javascript; charset=utf-8')

    def test_static_integration_css(self):
        css_files = [
            'swagger-ui.css',
            'index.css',
        ]

        for css in css_files:
            response = self.get_raw_link('{}/{}'.format(
                    self.base_static_path, css))
            self.assert_request_success(
                response, content_type='text/css; charset=utf-8')


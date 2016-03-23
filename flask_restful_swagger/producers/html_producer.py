# -*- coding: utf-8 -*-

import mimetypes
import os

from flask import url_for, redirect

__author__ = 'sobolevn'


class HtmlProducer(object):
    content_type = 'text/html'

    def __init__(self, swagger):
        self.swagger = swagger

    def get(self):
        index = url_for('SwaggerDocs.static', filename='index.html', )
        url = index + '?url=' + url_for('SwaggerDocs.json', _external=True)
        return redirect(url)

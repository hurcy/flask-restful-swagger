# -*- coding: utf-8 -*-

from flask import jsonify

__author__ = 'sobolevn'


class JsonProducer(object):
    content_type = 'application/json'

    def __init__(self, data):
        self.data = data

    def get(self):
        return jsonify({'apiVersion': '0.0.1'})

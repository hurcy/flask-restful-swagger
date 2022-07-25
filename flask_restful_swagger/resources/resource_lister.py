# -*- coding: utf-8 -*-

from flask_restful import Resource

from flask_restful_swagger.registry import get_current_registry

__author__ = 'sobolevn'


class ResourceLister(Resource):
    def get(self):
        req_registry = get_current_registry()
        path = req_registry['basePath']

        return {
            "info": req_registry['info'],
            "swagger": req_registry['swagger'],
            "apis": [{
                "path": path
            }]
        }

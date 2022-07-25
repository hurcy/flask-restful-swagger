# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger

from tests.apps import config
from tests.apps.shared_code import Todo, MarshalWithExample

__author__ = 'sobolevn'


api_meta = {
    "swagger": "2.0",
	"info": {
		"description": "This is a sample server",
		"version": "1.0.0",
		"title": "Swagger Test",
	},
	"host": "http://0.0.0.0:5001",
	"base_path": "/api/spec",
}

app = Flask(__name__, static_folder='../static')
app.config.from_object(config)

api = swagger.docs(Api(app), **api_meta)
api.add_resource(Todo, '/todo/<string:todo_id>')
api.add_resource(MarshalWithExample, '/marshal')

api.init_app(app)


from pprint import pprint
pprint(list(app.url_map.iter_rules()))
for route in app.url_map.iter_rules():
    print(route)

if __name__ == '__main__':
    app.run()

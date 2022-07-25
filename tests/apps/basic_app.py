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
		"description": "This is a sample server Petstore server.  You can find out more about Swagger at [http://swagger.io](http://swagger.io) or on [irc.freenode.net, #swagger](http://swagger.io/irc/).  For this sample, you can use the api key `special-key` to test the authorization filters.",
		"version": "1.0.6",
		"title": "Swagger Petstore",
	},
	"host": "http://0.0.0.0:5001",
	"base_path": "/api/spec",
}

app = Flask(__name__, static_folder='../static')
app.config.from_object(config)

api = swagger.docs(Api(app), **api_meta)
api.add_resource(Todo, '/todo/<string:todo_id>')
api.add_resource(MarshalWithExample, '/marshal')

if __name__ == '__main__':
    app.run()

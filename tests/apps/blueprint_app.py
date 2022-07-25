# -*- coding: utf-8 -*-

from flask import Flask, Blueprint
from flask_restful import Api
from flask_restful_swagger import swagger

from tests.apps import config
from tests.apps.shared_code import Todo, MarshalWithExample

__author__ = 'sobolevn'


api_meta_marshal = {
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

marshal_blueprint = Blueprint('marshal_blueprint', __name__)


api_marshal = swagger.docs(Api(marshal_blueprint), **api_meta_marshal)
api_marshal.add_resource(MarshalWithExample, '/marshal')

app.register_blueprint(marshal_blueprint, url_prefix='/api-marshal')



from pprint import pprint
pprint(list(app.url_map.iter_rules()))
# for route in app.url_map.iter_rules():
#     print(route)
    
if __name__ == '__main__':
    app.run()

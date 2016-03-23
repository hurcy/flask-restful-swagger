# -*- coding: utf-8 -*-

from flask import Flask
from flask.ext.restful import Api, fields
from flask_restful import Resource

from flask_restful_swagger import swagger as swg

from tests.apps import config


__author__ = 'sobolevn'


app = Flask(__name__, static_folder='../static')
app.config.from_object(config)


api_meta = {
    'apiVersion': '0.1',
    'resourcePath': '/',
    'produces': [
        'application/json',
        'text/html',
    ],
    'api_spec_url': '/api/spec',
    'description': 'A Basic API',
}

swagger = swg.docs(Api(app), **api_meta)


@swagger.model
class TodoItem(object):
    def __init__(self, arg1, arg2, arg3='123'):
        pass


@swagger.model
class ModelWithResourceFields(object):
    resource_fields = {
        'a_string': fields.String(),
    }


class Todo(Resource):
    """
    Todo-Description
    Todo-Notes
    """

    @swagger.operation(
        notes='get a todo item by ID',
        nickname='get',
        parameters=[{
            'name': 'todo_id_x',
            'description': 'The ID of the TODO item',
            'required': True,
            'allowMultiple': False,
            'dataType': 'string',
            'paramType': 'path',
        }, {
            'name': 'a_bool',
            'description': 'The ID of the TODO item',
            'required': True,
            'allowMultiple': False,
            'dataType': 'boolean',
            'paramType': 'path',
        }, ]
    )
    def get(self, todo_id):
        """Summary"""

        # We expect this method to be in our specs.
        return {
           'todo_item': '{}{}'.format('todo', todo_id)
        }, 200, {
            'Access-Control-Allow-Origin': '*',
        }


swagger.add_resource(Todo, '/todo/<string:todo_id>')
# swagger.add_resource(MarshalWithExample, '/marshal')


@app.route('/test')
def test():
    s = app
    return 'Done'

if __name__ == '__main__':
    app.run(debug=True)

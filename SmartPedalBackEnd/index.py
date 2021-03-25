# Flask-Restful API

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from marshmallow import Schema, fields

app = Flask(__name__)
api = Api(app)

PEDALS = {
    'pedal1': {'task': 'build an API'},
    'pedal2': {'task': '?????'},
    'pedal3': {'task': 'profit!'},
}


def abort_if_pedal_doesnt_exist(pedal_id):
    if pedal_id not in PEDALS:
        abort(404, message="Pedal {} doesn't exist".format(pedal_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Pedal
# shows a single pedal item and lets you delete a pedal item
class Pedal(Resource):
    def get(self, pedal_id):
        abort_if_pedal_doesnt_exist(pedal_id)
        return PEDALS[pedal_id]

    def delete(self, pedal_id):
        abort_if_pedal_doesnt_exist(pedal_id)
        del PEDALS[pedal_id]
        return '', 204

    def put(self, pedal_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        PEDALS[pedal_id] = task
        return task, 201


# PedalList
# shows a list of all pedals, and lets you POST to add new tasks
class PedalList(Resource):
    def get(self):
        return PEDALS

    def post(self):
        args = parser.parse_args()
        pedal_id = int(max(PEDALS.keys()).lstrip('pedal')) + 1
        pedal_id = 'pedal%i' % pedal_id
        PEDALS[pedal_id] = {'task': args['task']}
        return PEDALS[pedal_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(PedalList, '/pedals')
api.add_resource(Pedal, '/pedals/<pedal_id>')


if __name__ == '__main__':
    app.run(debug=True)
from server import Server
# import os
# import logging
from flask import Flask
from flask_restful import Resource, Api
from webargs import fields
from webargs.flaskparser import use_args
server = Server()
app = Flask(__name__)
api = Api(app)


class Schedule(Resource):
    def get(self):
        return {"response_schedule": server.schedule_query.get_schedule()}


api.add_resource(Schedule, '/schedule')

if __name__ == "__main__":
    app.run(host="192.168.0.101", debug=True)

#
# file_dir = os.path.split(os.path.realpath(__file__))[0]
# file_name = file_dir + '\logs.txt'
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p', filename=file_name, level=logging.INFO)
# server.setup()

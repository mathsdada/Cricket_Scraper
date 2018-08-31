from aiohttp import web
import socketio
from database.database_engine import Database
from interface import Query, Response
import json


class Server:
    def __init__(self):
        self.num_clients = 0
        # setup database connection for handling client queries
        self.database = Database("localhost", "cricbuzz", "mathsdada", "1@gangadhar")
        self.database.connect()

    def setup(self):
        sio = socketio.AsyncServer()
        app = web.Application()
        sio.attach(app)
        web.run_app(app, host='192.168.0.104', port=5678)

        @sio.on('connect', namespace='/')
        def connect(sid):
            self.event_handler('connect', sid)

        @sio.on('disconnect', namespace='/')
        def disconnect(sid):
            self.event_handler('disconnect', sid)

        @sio.on('query', namespace='/')
        async def query(sid, data):
            response = self.event_handler('query', data)
            await sio.emit('response', response, room=sid)

    def event_handler(self, event_type, event_data):
        response = None
        if event_type == 'connect':
            self.num_clients += 1
        elif event_type == 'disconnect':
            self.num_clients -= 1
        elif event_type == 'query':
            query_json = json.loads(event_data)
            query_type = query_json['type']
            query_data = query_json['data']
            response = self.handle_query(query_type, query_data)
        else:
            pass
        return response

    def handle_query(self, query_type, query_data):
        if query_type == Query.SCHEDULE:
            response_type = Response.SCHEDULE
            response_data = None
        else:
            response_type = None
            response_data = None
        response = {'type': response_type, 'data': response_data}
        return response

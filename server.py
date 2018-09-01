from aiohttp import web
import socketio
from database.database_engine import Database
from interface import Query, Response
import json
from database.query.schedule import Schedule
from database.query.player import Player
from database.query.venue import Venue
from database.query.team import Team

class Server:
    def __init__(self):
        self.num_clients = 0
        # setup database connection for handling client queries
        self.database = Database("localhost", "cricbuzz", "mathsdada", "1@gangadhar")
        self.database.connect()

        # query objects
        self.schedule_query = Schedule(self.database.cursor)
        self.player_query = Player(self.database.cursor)
        self.venue_query = Venue(self.database.cursor)
        self.team_query = Team(self.database.cursor)

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
            response_data = self.schedule_query.get_schedule()
        else:
            response_type = None
            response_data = None
        response = {'type': response_type, 'data': response_data}
        return response

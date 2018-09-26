import logging
import os
from aiohttp import web
import socketio
from database.database_engine import Database
from interface import Interface
import json
from database.query.schedule import Schedule
from database.query.player import Player
from database.query.venue import Venue
from database.query.team import Team
from controller import Controller


class Server:
    def __init__(self):
        self.logger = logging.getLogger("Dream:Server")
        self.num_clients = 0
        self.database = Database()
        self.database.connect()

        # query objects
        self.schedule_query = Schedule(self.database.cursor)
        self.player_query = Player(self.database.cursor)
        self.venue_query = Venue(self.database.cursor)
        self.team_query = Team(self.database.cursor)

        # Controller
        self.controller = Controller(self.database)
        # self.update_database()

    def update_database(self):
        self.controller.update_stats_database()
        self.controller.update_schedule_database()
        # start a timer to next scraping time..

    def setup(self):
        sio = socketio.AsyncServer()
        app = web.Application()
        sio.attach(app)

        @sio.on('connect', namespace='/')
        def connect(sid, env):
            self.event_handler('connect', sid)

        @sio.on('disconnect', namespace='/')
        def disconnect(sid):
            self.event_handler('disconnect', sid)

        @sio.on('query', namespace='/')
        async def query(sid, data):
            self.logger.info("query from client ({})-  {}".format(sid, data))
            response = self.event_handler('query', data)
            self.logger.info("response to client ({})-  {}".format(sid, response))
            await sio.emit('response', response, room=sid)

        web.run_app(app, host='192.168.0.105', port=5678)

    def event_handler(self, event_type, event_data):
        response = None
        if event_type == 'connect':
            self.logger.info("Client Connected : {}".format(event_data))
            self.num_clients += 1
        elif event_type == 'disconnect':
            self.logger.info("Client Disconnected : {}".format(event_data))
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
        if query_type == Interface.QUERY_SCHEDULE:
            response_type = Interface.RESP_SCHEDULE
            response_data = self.schedule_query.get_schedule()
        elif query_type == Interface.QUERY_TEAM_STATS:
            query_data = json.loads(query_data)
            response_type = Interface.RESP_TEAM_STATS
            response_data = []
            format = query_data['format']
            teams = query_data['teams']
            for team in teams:
                team_name = team['team_name']
                team_stats = self.team_query.get_team_stats(format, team_name)
                response_data.append({'team_name': team_name,
                                      'team_stats': team_stats})
        else:
            response_type = None
            response_data = None
        response = {'type': response_type, 'data': response_data}
        return response


# file_dir = os.path.split(os.path.realpath(__file__))[0]
# file_name = file_dir + '\logs.txt'
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p', filename=file_name, level=logging.INFO)
# server = Server()
# server.setup()

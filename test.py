from server import Server
from flask import Flask, json
from flask_restful import Resource, Api, reqparse

server = Server()
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class Schedule(Resource):
    def get(self):
        return {"response_schedule": server.schedule_query.get_schedule()}


class TeamStatsRecentForm(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument("format")
        args = parser.parse_args()
        return server.team_query.get_team_form(
            args['team_name'], args['venue_name'], args['format'])


class TeamStatsBattingMostRuns(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_batting_most_runs(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBattingBestStrikeRate(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_best_batting_strike_rate(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBattingMost50s(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_most_50s(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBattingMost100s(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_most_100s(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBattingMost4s(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_most_4s(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBattingMost6s(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_most_6s(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBattingMostDucks(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_most_ducks(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBattingHighScores(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_high_scores(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBowlingMostWickets(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_most_wickets(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBowlingBestEconomy(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_best_bowling_economy(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBowlingBestStrikeRate(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_best_bowling_strike_rate(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBowlingMostFourPlusWickets(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_most_4_plus_wickets(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBowlingMostFivePlusWickets(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_most_5_plus_wickets(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBowlingMostMaidens(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_most_maidens(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBowlingBestFigureInnings(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_best_bowling_figure_in_innings(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsBowlingMostRunsConcededInnings(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')
        args = parser.parse_args()
        return server.team_query.get_most_runs_conceded_in_innings(
            args['team_name'], args['venue_name'], args['format'], args['squad'])


class TeamStatsHeadToHeadRunsVsBowlingStyles(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')  # Batsmen
        parser.add_argument('squad-2', action='append')  # Bowling Styles
        args = parser.parse_args()
        return server.team_query.get_runs_against_bowling_styles(
            args['team_name'], args['venue_name'], args['format'], args['squad'], args['squad-2'])


class TeamStatsHeadToHeadRunsVsBowlers(Resource):
    def post(self):
        parser.add_argument('team_name')
        parser.add_argument('venue_name')
        parser.add_argument('format')
        parser.add_argument('squad', action='append')  # Batsmen
        parser.add_argument('squad-2', action='append')  # Bowlers
        args = parser.parse_args()
        return server.team_query.get_runs_against_bowlers(
            args['team_name'], args['venue_name'], args['format'], args['squad'], args['squad-2'])


# Schedule
api.add_resource(Schedule, '/schedule')

# Team Stats
api.add_resource(TeamStatsRecentForm, '/team_stats/recent_form')

api.add_resource(TeamStatsBattingMostRuns, '/team_stats/batting/most_runs')
api.add_resource(TeamStatsBattingBestStrikeRate, '/team_stats/batting/best_strike_rate')
api.add_resource(TeamStatsBattingMost50s, '/team_stats/batting/most_50s')
api.add_resource(TeamStatsBattingMost100s, '/team_stats/batting/most_100s')
api.add_resource(TeamStatsBattingMost4s, '/team_stats/batting/most_4s')
api.add_resource(TeamStatsBattingMost6s, '/team_stats/batting/most_6s')
api.add_resource(TeamStatsBattingMostDucks, '/team_stats/batting/most_0s')
api.add_resource(TeamStatsBattingHighScores, '/team_stats/batting/high_scores')

api.add_resource(TeamStatsBowlingMostWickets, '/team_stats/bowling/most_wickets')
api.add_resource(TeamStatsBowlingBestEconomy, '/team_stats/bowling/best_economy')
api.add_resource(TeamStatsBowlingBestStrikeRate, '/team_stats/bowling/best_strike_rate')
api.add_resource(TeamStatsBowlingMostFourPlusWickets, '/team_stats/bowling/most_4_plus_wickets')
api.add_resource(TeamStatsBowlingMostFivePlusWickets, '/team_stats/bowling/most_5_plus_wickets')
api.add_resource(TeamStatsBowlingMostMaidens, '/team_stats/bowling/most_maidens')
api.add_resource(TeamStatsBowlingBestFigureInnings, '/team_stats/bowling/best_bowling_in_innings')
api.add_resource(TeamStatsBowlingMostRunsConcededInnings, '/team_stats/bowling/most_runs_conceded_in_innings')

api.add_resource(TeamStatsHeadToHeadRunsVsBowlingStyles, '/team_stats/head_to_head/runs_against_bowling_styles')
api.add_resource(TeamStatsHeadToHeadRunsVsBowlers, '/team_stats/head_to_head/runs_against_bowlers')

# Player Stats


if __name__ == "__main__":
    app.run(host="192.168.0.104", debug=True)

#
# file_dir = os.path.split(os.path.realpath(__file__))[0]
# file_name = file_dir + '\logs.txt'
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p', filename=file_name, level=logging.INFO)
# server.setup()

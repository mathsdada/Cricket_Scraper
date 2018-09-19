from scraper.scraper_stats import StatsScraper
from database.database_engine import Database
from database.schema.player import Player
from database.schema.series import Series
from database.schema.match import Match
from database.schema.team import Team
from database.schema.innings_stats import InningsStats
from database.schema.head_to_head_stats import HeadToHeadStats
from database.schema.batting_stats import BattingStats
from database.schema.bowling_stats import BowlingStats
from scraper.scraper_schedule import ScheduleScraper
from database.schema.schedule_series import Series as ScheduleSeries
from database.schema.schedule_match import Match as ScheduleMatch
from database.schema.schedule_team import Team as ScheduleTeam
from database.schema.schedule_player import Player as SchedulePlayer


class Controller:
    def __init__(self, database):
        self.database = database

    def update_stats_database(self):
        scraper = StatsScraper()
        calender_year = scraper.get_stats_of_calender_year(2018)

        player_table = Player(self.database.cursor)
        series_table = Series(self.database.cursor)
        team_table = Team(self.database.cursor)
        match_table = Match(self.database.cursor)
        innings_stats_table = InningsStats(self.database.cursor)
        head_to_head_stats_table = HeadToHeadStats(self.database.cursor)
        bowling_stats_table = BowlingStats(self.database.cursor)
        batting_stats_table = BattingStats(self.database.cursor)

        for series in calender_year.get_series_list():
            series_table.insert(series.series_id, series.series_title, series.gender, series.series_year)
            for match in series.get_matches_list():
                team_name_id_map = {}
                for team_name in match.teams:
                    team_id = team_table.insert(team_name, match.teams[team_name])
                    team_name_id_map[team_name] = team_id
                winning_team_id = None
                if match.winning_team in team_name_id_map:
                    winning_team_id = team_name_id_map[match.winning_team]
                match_table.insert(match.id, match.title, match.date, match.format, match.venue,
                                   match.outcome, series.series_id, series.gender,
                                   list(team_name_id_map.values()), winning_team_id)
                for innings_score in match.get_match_innings_scores():
                    innings_stats_table.insert(match.id, innings_score.number, innings_score.runs_scored,
                                               innings_score.wickets_lost,
                                               innings_score.overs_played,
                                               team_name_id_map[innings_score.batting_team],
                                               team_name_id_map[innings_score.bowling_team])
                    for batting_score in innings_score.get_batting_scores():
                        batsman_profile = match.squad[batting_score.player_name]
                        player_table.insert(batsman_profile.player_id, batsman_profile.name, batsman_profile.role,
                                            batsman_profile.batting_style, batsman_profile.bowling_style, series.gender)
                        batting_stats_table.insert(batsman_profile.player_id, match.id, innings_score.number,
                                                   batting_score.runs_scored, batting_score.balls_played,
                                                   batting_score.num_fours, batting_score.num_sixes,
                                                   team_name_id_map[innings_score.batting_team])
                    for bowling_score in innings_score.get_bowling_scores():
                        bowler_profile = match.squad[bowling_score.player_name]
                        player_table.insert(bowler_profile.player_id, bowler_profile.name, bowler_profile.role,
                                            bowler_profile.batting_style, bowler_profile.bowling_style, series.gender)
                        bowling_stats_table.insert(bowler_profile.player_id, match.id, innings_score.number,
                                                   bowling_score.wickets_taken, bowling_score.overs_bowled,
                                                   bowling_score.runs_given, bowling_score.economy,
                                                   team_name_id_map[innings_score.bowling_team])
                for head_to_head in match.get_head_to_head_data():
                    batsman_profile = match.squad[head_to_head.batsman]
                    bowler_profile = match.squad[head_to_head.bowler]
                    player_table.insert(batsman_profile.player_id, batsman_profile.name, batsman_profile.role,
                                        batsman_profile.batting_style, batsman_profile.bowling_style, series.gender)
                    player_table.insert(bowler_profile.player_id, bowler_profile.name, bowler_profile.role,
                                        bowler_profile.batting_style, bowler_profile.bowling_style, series.gender)
                    head_to_head_stats_table.insert(bowler_profile.player_id, batsman_profile.player_id, match.id,
                                                    head_to_head.runs, head_to_head.balls, head_to_head.wickets)
                self.database.conn.commit()

    def update_schedule_database(self):
        self.__clear_schedule_database()
        scraper = ScheduleScraper()

        series_table = ScheduleSeries(self.database.cursor)
        match_table = ScheduleMatch(self.database.cursor)
        team_table = ScheduleTeam(self.database.cursor)
        player_table = SchedulePlayer(self.database.cursor)

        for series in scraper.get_schedule():
            series_table.insert(series.id, series.title, series.gender)
            for match in series.get_matches_list():
                team_ids = []
                for team in match.teams:
                    player_objects = match.teams[team]['squad']
                    player_ids = []
                    for player_object in player_objects:
                        player_table.insert(player_object.player_id, player_object.name, player_object.role,
                                            player_object.batting_style, player_object.bowling_style,
                                            series.gender)
                        player_ids.append(int(player_object.player_id))
                    team_ids.append(
                        team_table.insert(team, match.teams[team]['short_name'], player_ids))
                match_table.insert(match.id, match.title, match.format, match.time, match.venue,
                                   team_ids,
                                   series.id, series.gender)
        self.database.conn.commit()

    def __clear_schedule_database(self):
        series_table = ScheduleSeries(self.database.cursor)
        match_table = ScheduleMatch(self.database.cursor)
        team_table = ScheduleTeam(self.database.cursor)
        player_table = SchedulePlayer(self.database.cursor)

        match_table.clear()
        series_table.clear()
        team_table.clear()
        player_table.clear()

        self.database.conn.commit()

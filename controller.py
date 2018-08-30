import os
import logging
from scraper.scraper_stats import StatsScraper
from database.database_engine import Database
from database.schema.player import Player
from database.schema.series import Series
from database.schema.match import Match
from database.schema.innings_stats import InningsStats
from database.schema.head_to_head_stats import HeadToHeadStats
from database.schema.batting_stats import BattingStats
from database.schema.bowling_stats import BowlingStats
from scraper.scraper_schedule import ScheduleScraper
from database.schema.schedule_series import Series as ScheduleSeries
from database.schema.schedule_match import Match as ScheduleMatch
from database.schema.schedule_squad import Squad as ScheduleSquad


class Controller:
    def __init__(self):
        file_dir = os.path.split(os.path.realpath(__file__))[0]
        file_name = file_dir + '\logs.txt'
        logging.basicConfig(filename=file_name, level=logging.INFO)

    def update_stats_database(self):
        scraper = StatsScraper()
        calender_year = scraper.get_stats_of_calender_year(2018)

        database = Database("localhost", "cricbuzz", "mathsdada", "1@gangadhar")
        database.connect()
        player_table = Player(database.cursor)
        series_table = Series(database.cursor)
        match_table = Match(database.cursor)
        innings_stats_table = InningsStats(database.cursor)
        head_to_head_stats_table = HeadToHeadStats(database.cursor)
        bowling_stats_table = BowlingStats(database.cursor)
        batting_stats_table = BattingStats(database.cursor)

        for series in calender_year.get_series_list():
            series_table.insert(series.series_id, series.series_title, series.gender, series.series_year)
            for match in series.get_matches_list():
                match_table.insert(match.id, match.title, match.date, match.format, match.venue,
                                   match.teams, match.winning_team, match.outcome, series.series_id, series.gender)
                for innings_score in match.get_match_innings_scores():
                    innings_stats_table.insert(match.id, innings_score.number, innings_score.batting_team,
                                               innings_score.bowling_team, innings_score.runs_scored,
                                               innings_score.wickets_lost,
                                               innings_score.overs_played)
                    for batting_score in innings_score.get_batting_scores():
                        batsman_profile = match.squad[batting_score.player_name]
                        player_table.insert(batsman_profile.player_id, batsman_profile.name, batsman_profile.role,
                                            batsman_profile.batting_style, batsman_profile.bowling_style, series.gender)
                        batting_stats_table.insert(batsman_profile.player_id, match.id, innings_score.number,
                                                   batting_score.runs_scored, batting_score.balls_played,
                                                   batting_score.num_fours, batting_score.num_sixes,
                                                   innings_score.batting_team)
                    for bowling_score in innings_score.get_bowling_scores():
                        bowler_profile = match.squad[bowling_score.player_name]
                        player_table.insert(bowler_profile.player_id, bowler_profile.name, bowler_profile.role,
                                            bowler_profile.batting_style, bowler_profile.bowling_style, series.gender)
                        bowling_stats_table.insert(bowler_profile.player_id, match.id, innings_score.number,
                                                   bowling_score.wickets_taken, bowling_score.overs_bowled,
                                                   bowling_score.runs_given, bowling_score.economy,
                                                   innings_score.bowling_team)
                for head_to_head in match.get_head_to_head_data():
                    batsman_profile = match.squad[head_to_head.batsman]
                    bowler_profile = match.squad[head_to_head.bowler]
                    player_table.insert(batsman_profile.player_id, batsman_profile.name, batsman_profile.role,
                                        batsman_profile.batting_style, batsman_profile.bowling_style, series.gender)
                    player_table.insert(bowler_profile.player_id, bowler_profile.name, bowler_profile.role,
                                        bowler_profile.batting_style, bowler_profile.bowling_style, series.gender)
                    head_to_head_stats_table.insert(bowler_profile.player_id, batsman_profile.player_id, match.id,
                                                    head_to_head.runs, head_to_head.balls, head_to_head.wickets)
                database.conn.commit()
        database.close()

    def update_schedule_database(self):
        self.clear_schedule_database()

        scraper = ScheduleScraper()

        database = Database("localhost", "cricbuzz", "mathsdada", "1@gangadhar")
        database.connect()
        series_table = ScheduleSeries(database.cursor)
        match_table = ScheduleMatch(database.cursor)
        squad_table = ScheduleSquad(database.cursor)

        for series in scraper.get_schedule():
            series_table.insert(series.id, series.title, series.gender)
            for match in series.get_matches_list():
                match_table.insert(match.id, match.title, match.format, match.time, match.venue, list(match.teams.keys()),
                                   series.id, series.gender)
                for team in match.teams:
                    squad_table.insert(match.id, team, match.teams[team])
        database.conn.commit()
        database.close()

    def clear_schedule_database(self):
        database = Database("localhost", "cricbuzz", "mathsdada", "1@gangadhar")
        database.connect()

        series_table = ScheduleSeries(database.cursor)
        match_table = ScheduleMatch(database.cursor)
        squad_table = ScheduleSquad(database.cursor)

        squad_table.clear()
        match_table.clear()
        series_table.clear()

        database.conn.commit()
        database.close()
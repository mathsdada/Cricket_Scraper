from scraper_engine.scraper import Scraper
from database_engine.database import Database
from database_engine.model.player import Player
from database_engine.model.series import Series
from database_engine.model.match import Match
from database_engine.model.innings_stats import InningsStats
from database_engine.model.head_to_head_stats import HeadToHeadStats
from database_engine.model.batting_stats import BattingStats
from database_engine.model.bowling_stats import BowlingStats

scraper = Scraper()
calender_year = scraper.get_data(2018)

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
    series_table.insert(series.series_id, series.series_title, series.series_year)
    for match in series.get_matches_list():
        match_table.insert(match.id, match.title, match.date, match.format, match.venue,
                           match.teams,
                           match.winning_team, match.outcome, series.series_id)
        for innings_score in match.get_match_innings_scores():
            innings_stats_table.insert(match.id, innings_score.number, innings_score.batting_team,
                                       innings_score.bowling_team, innings_score.runs_scored,
                                       innings_score.wickets_lost,
                                       innings_score.overs_played)
            for batting_score in innings_score.get_batting_scores():
                batsman_profile = match.squad[batting_score.player_id]
                player_table.insert(batsman_profile.player_id, batsman_profile.name, batsman_profile.role,
                                    batsman_profile.batting_style, batsman_profile.bowling_style)
                batting_stats_table.insert(batting_score.player_id, match.id, innings_score.number,
                                           batting_score.runs_scored, batting_score.balls_played,
                                           batting_score.num_fours, batting_score.num_sixes, innings_score.batting_team)
            for bowling_score in innings_score.get_bowling_scores():
                bowler_profile = match.squad[bowling_score.player_id]
                player_table.insert(bowler_profile.player_id, bowler_profile.name, bowler_profile.role,
                                    bowler_profile.batting_style, bowler_profile.bowling_style)
                bowling_stats_table.insert(bowling_score.player_id, match.id, innings_score.number,
                                           bowling_score.wickets_taken, bowling_score.overs_bowled,
                                           bowling_score.runs_given, bowling_score.economy, innings_score.bowling_team)
        for head_to_head in match.get_head_to_head_data():
            pass

database.conn.commit()
database.close()

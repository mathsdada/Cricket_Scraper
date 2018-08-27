from scraper.common_util import Common
from scraper.model.stats.batsman_score import BatsmanScore
from scraper.model.stats.bowler_score import BowlerScore
from scraper.model.stats.commentary import Commentary
from scraper.model.stats.innings_score import InningsScore
from scraper.model.stats.player import Player
from datetime import datetime
import threading
import logging


class Match:
    def __init__(self, match_id, title, format, teams, venue, result, match_link, winning_team):
        self.id = match_id
        self.title = title
        self.format = format
        self.teams = teams
        self.venue = venue
        self.outcome = result
        self.match_link = match_link
        self.date = 0  # epoch time
        self.winning_team = winning_team
        self.squad = {}
        self.innings_scores = []
        self.head_to_head_data = []
        self.is_valid = True
        self.logger = logging.getLogger(__name__)

    def extract_match_data(self, series_squad):
        self.logger.info(
            "extract_match_data: match_link = {}, thread = {}".format(self.match_link, threading.current_thread().name))
        self.__extract_match_info_squad_and_scores(series_squad)
        self.__extract_head_to_head_data()

    def get_match_innings_scores(self):
        return self.innings_scores

    def get_head_to_head_data(self):
        return self.head_to_head_data

    def __extract_match_info(self, soup):
        match_info_blocks = soup.find_all('div', class_='cb-col cb-col-73')
        # Examples: 1) Friday, January 05, 2018 - Tuesday, January 09, 2018
        #           2) Tuesday, February 13, 2018
        match_date_string = match_info_blocks[1].text.split(" - ")[0].strip()
        self.date = datetime.strptime(match_date_string, "%A, %B %d, %Y").strftime("%Y-%m-%d")

    def __extract_match_squad(self, soup, series_squad):
        player_blocks = soup.find_all('a', class_='margin0 text-black text-hvr-underline')
        for player_block in player_blocks:
            player_id = player_block.get('href').split("/")[2]
            player_name = player_block.text
            player_name = Common.correct_player_name(player_name)
            if player_name not in series_squad.keys():
                series_squad[player_name] = Player(player_name, player_id)
            self.squad[player_name] = series_squad[player_name]
        self.logger.info("Squad => {} {}: {}".format(threading.current_thread().name, self.title, self.squad.keys()))

    def __extract_match_info_squad_and_scores(self, series_squad):
        match_score_card_link = Common.home_page + "/api/html/cricket-scorecard/" + str(self.id)
        soup = Common.get_soup_object(match_score_card_link)
        # Extract Match Info
        self.__extract_match_info(soup)
        # Extract Match Squad
        self.__extract_match_squad(soup, series_squad)
        # Extract Per-Innings Scores
        team_innings = soup.find_all('div', id=True)
        for innings_num, innings_data in enumerate(team_innings):
            innings_bat_bowl_blocks = innings_data.find_all('div', class_='cb-col cb-col-100 cb-ltst-wgt-hdr')
            innings_batting_block = innings_bat_bowl_blocks[0]
            innings_bowling_block = innings_bat_bowl_blocks[1]
            innings_score_object = self.__extract_innings_total_score(innings_batting_block, innings_num, self.teams)
            innings_score_object.set_batting_scores(self.__extract_innings_batting_scores(innings_batting_block))
            innings_score_object.set_bowling_scores(self.__extract_innings_bowling_scores(innings_bowling_block))
            self.innings_scores.append(innings_score_object)

    def __extract_head_to_head_data(self):
        commentary = Commentary(self.match_link, self.squad)
        self.head_to_head_data = commentary.get_head_to_head_data()

    def __extract_innings_total_score(self, innings_batting_block, innings_num, playing_teams):
        innings_score_block = innings_batting_block.find('div', class_='cb-col cb-col-100 cb-scrd-hdr-rw').text
        innings_data = innings_score_block.split(" Innings ")
        batting_team = innings_data[0].replace(" 1st", "").replace(" 2nd", "").strip()
        runs_scored = innings_data[1].split(u'\xa0')[0].split("-")[0]
        wickets_lost = innings_data[1].split(u'\xa0')[0].split("-")[1]
        overs_played = innings_data[1].split(u'\xa0')[1].replace("(", "").replace(")", "").strip()
        if batting_team == playing_teams[0]:
            bowling_team = playing_teams[1]
        else:
            bowling_team = playing_teams[0]
        return InningsScore(innings_num, batting_team, bowling_team, runs_scored, wickets_lost, overs_played)

    def __extract_innings_batting_scores(self, innings_batting_block):
        batsman_score_blocks = innings_batting_block.find_all('div', class_='cb-col cb-col-100 cb-scrd-itms')
        batsman_objects = []
        for batsman_score_block in batsman_score_blocks:
            player_info_block = batsman_score_block.find('div', class_='cb-col cb-col-27 ')
            if player_info_block is not None:
                player_name = Common.correct_player_name(player_info_block.text)
                runs_scored = batsman_score_block.find('div',
                                                       class_='cb-col cb-col-8 text-right text-bold').text.strip()
                # (balls, fours, sixes, strikeRate)
                other_score_blocks = batsman_score_block.find_all('div', class_='cb-col cb-col-8 text-right')
                balls_played = other_score_blocks[0].text.strip()
                num_fours = other_score_blocks[1].text.strip()
                num_sixes = other_score_blocks[2].text.strip()

                batsman_objects.append(BatsmanScore(player_name, runs_scored, balls_played, num_fours, num_sixes))
        return batsman_objects

    def __extract_innings_bowling_scores(self, innings_bowling_block):
        bowler_score_blocks = innings_bowling_block.find_all('div', class_='cb-col cb-col-100 cb-scrd-itms ')
        bowler_objects = []
        for bowler_score_block in bowler_score_blocks:
            player_info_block = bowler_score_block.find('div', class_='cb-col cb-col-40')
            if player_info_block is not None:
                player_name = Common.correct_player_name(player_info_block.text)
                wickets_taken = bowler_score_block.find('div',
                                                        class_='cb-col cb-col-8 text-right text-bold').text.strip()
                # Runs Given and Economy
                runs_and_economy_blocks = bowler_score_block.find_all('div', class_='cb-col cb-col-10 text-right')
                runs_given = runs_and_economy_blocks[0].text.strip()
                economy = runs_and_economy_blocks[1].text.strip()
                # Overs Bowled, Maiden Overs, No Balls, Wide Balls
                other_score_items = bowler_score_block.find_all('div', class_='cb-col cb-col-8 text-right')
                overs_bowled = other_score_items[0].text.strip()

                if len(economy) != 0:
                    # Reason : Wasim Jaffer : https://www.cricbuzz.com/live-cricket-scorecard/19085/vidarbha-vs-chhattisgarh-group-d-ranji-trophy-2017-18
                    bowler_objects.append(BowlerScore(player_name, overs_bowled, wickets_taken, runs_given, economy))
        return bowler_objects

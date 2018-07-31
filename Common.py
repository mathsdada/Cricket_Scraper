import requests
from bs4 import BeautifulSoup


class Common:
    home_page = "http://www.cricbuzz.com"
    match_formats = ["T20", "ODI", "TEST"]

    @staticmethod
    def get_soup_object(link, retry_count=0):
        try:
            html_page = requests.get(link)
            if html_page.status_code == 200:
                return BeautifulSoup(html_page.text, 'html.parser')
            else:
                return None
        except requests.exceptions.RequestException as e:
            retry_count += 1
            if retry_count <= 5:
                print("Retrying: " + link + " Retry Count : " + str(retry_count))
                return Common.get_soup_object(link, retry_count)
            else:
                print("Max retries reached.")
                return None

    @staticmethod
    def get_match_format(match_title, series_formats):
        match_type = match_title.split(",")[1].lower()
        series_formats = series_formats.lower()
        if "practice" in match_title or "warm-up" in match_title:
            return "UNKNOWN"
        elif " t20" in match_type:
            return Common.match_formats[0]
        elif " odi" in match_type:
            return Common.match_formats[1]
        elif " test" in match_type:
            return Common.match_formats[2]
        elif " t20" in series_formats:
            return Common.match_formats[0]
        elif " odi" in series_formats:
            return Common.match_formats[1]
        elif " test" in series_formats:
            return Common.match_formats[2]
        else:
            return "UNKNOWN"

    @staticmethod
    def get_match_outcome(match_outcome):
        result_pattern = ["match tied", " won by ", "match drawn", " abandoned", "no result"]
        result_type = ["TIE", "WIN", "DRAW", "NO RESULT", "NO RESULT"]
        match_outcome = match_outcome.lower()
        for index, pattern in enumerate(result_pattern):
            if pattern in match_outcome:
                return result_type[index]

    @staticmethod
    def get_match_winning_team(match_status, match_result):
        if match_status == "WIN":
            if " won by " in match_result:
                match_winner = match_result.split(" won by ")[0]
            else:
                match_winner = match_result.split(" Won by ")[0]
        else:
            match_winner = ""
        return match_winner


class Player:
    def __init__(self, name, player_id, role="--"):
        self.name = name
        self.player_id = player_id
        self.role = role


class Batsman:
    def __init__(self, player=None, runs_scored=0, balls_played=0, num_fours=0, num_sixes=0):
        self.player = player
        self.runs_scored = runs_scored
        self.balls_played = balls_played
        self.num_fours = num_fours
        self.num_sixes = num_sixes


class Bowler:
    def __init__(self, player, overs_bowled, wickets_taken, runs_given, economy):
        self.player = player
        self.overs_bowled = overs_bowled
        self.wickets_taken = wickets_taken
        self.runs_given = runs_given
        self.economy = economy


class InningsScore:
    def __init__(self, number, batting_team, bowling_team,
                 runs_scored, wickets_lost, overs_played,
                 batting_scores=None, bowling_scores=None):
        if batting_scores is None:
            batting_scores = []
        if bowling_scores is None:
            bowling_scores = []
        self.number = number
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        self.runs_scored = runs_scored
        self.wickets_lost = wickets_lost
        self.overs_played = overs_played
        self.batting_scores = batting_scores
        self.bowling_scores = bowling_scores

    def set_batting_scores(self, batting_scores):
        self.batting_scores = batting_scores

    def set_bowling_scores(self, bowling_scores):
        self.bowling_scores = bowling_scores


class Match:
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
                player_id = player_info_block.find('a', href=True).get('href').split("/")[2]
                player_name = player_info_block.text.strip().split(" (c)")[0].split(" (wk)")[0]
                runs_scored = batsman_score_block.find('div',
                                                       class_='cb-col cb-col-8 text-right text-bold').text.strip()
                # (balls, fours, sixes, strikeRate)
                other_score_blocks = batsman_score_block.find_all('div', class_='cb-col cb-col-8 text-right')
                balls_played = other_score_blocks[0].text.strip()
                num_fours = other_score_blocks[1].text.strip()
                num_sixes = other_score_blocks[2].text.strip()

                player_object = Player(player_name, player_id)
                batsman_objects.append(Batsman(player_object, runs_scored, balls_played, num_fours, num_sixes))
        return batsman_objects

    def __extract_innings_bowling_scores(self, innings_bowling_block):
        bowler_score_blocks = innings_bowling_block.find_all('div', class_='cb-col cb-col-100 cb-scrd-itms ')
        bowler_objects = []
        for bowler_score_block in bowler_score_blocks:
            player_info_block = bowler_score_block.find('div', class_='cb-col cb-col-40')
            if player_info_block is not None:
                player_id = player_info_block.find('a', href=True).get('href').split("/")[2]
                player_name = player_info_block.text.strip().split(" (c)")[0].split(" (wk)")[0]
                wickets_taken = bowler_score_block.find('div',
                                                        class_='cb-col cb-col-8 text-right text-bold').text.strip()
                # Runs Given and Economy
                runs_and_economy_blocks = bowler_score_block.find_all('div', class_='cb-col cb-col-10 text-right')
                runs_given = runs_and_economy_blocks[0].text.strip()
                economy = runs_and_economy_blocks[1].text.strip()
                # Overs Bowled, Maiden Overs, No Balls, Wide Balls
                other_score_items = bowler_score_block.find_all('div', class_='cb-col cb-col-8 text-right')
                overs_bowled = other_score_items[0].text.strip()

                player_object = Player(player_name, player_id)
                bowler_objects.append(Bowler(player_object, overs_bowled, wickets_taken, runs_given, economy))
        return bowler_objects

    def __extract_match_scores(self):
        match_score_card_link = Common.home_page + "/api/html/cricket-scorecard/" + str(self.match_id)
        soup = Common.get_soup_object(match_score_card_link)
        team_innings = soup.find_all('div', id=True)
        for innings_num, innings_data in enumerate(team_innings):
            innings_bat_bowl_blocks = innings_data.find_all('div', class_='cb-col cb-col-100 cb-ltst-wgt-hdr')
            innings_batting_block = innings_bat_bowl_blocks[0]
            innings_bowling_block = innings_bat_bowl_blocks[1]
            innings_score_object = self.__extract_innings_total_score(innings_batting_block, innings_num, self.teams)
            innings_score_object.set_batting_scores(self.__extract_innings_batting_scores(innings_batting_block))
            innings_score_object.set_bowling_scores(self.__extract_innings_bowling_scores(innings_bowling_block))
            self.innings_scores.append(innings_score_object)

    def __init__(self, match_id, title,
                 format, teams, venue, result, match_link):
        self.match_id = match_id
        self.title = title
        self.format = format
        self.teams = teams
        self.venue = venue
        self.result = result
        self.match_link = match_link
        self.innings_scores = []
        self.__extract_match_scores()

    def get_match_scores(self):
        return self.innings_scores


class Series:
    def __extract_matches_list_of_series(self):
        soup = Common.get_soup_object(self.series_link)
        series_formats = \
            soup.find('div', class_='cb-col-100 cb-col cb-nav-main cb-bg-white').find('div').text.split(".")[0]
        match_info_elements = soup.find_all('div', class_='cb-col-60 cb-col cb-srs-mtchs-tm')
        for match_info_element in match_info_elements:
            match_title = match_info_element.find('a', class_='text-hvr-underline')
            match_venue = match_info_element.find('div')
            match_result = match_info_element.find('a', class_='cb-text-link')
            if (match_title is not None) and ("cricket-scores" in match_title.get('href')) and \
                    (match_venue is not None) and (match_result is not None):
                print(match_title.text)
                match_format = Common.get_match_format(match_title.text, series_formats)
                if match_format in Common.match_formats:
                    match_link = match_title.get('href')
                    match_title = match_title.text
                    match_status = Common.get_match_outcome(match_result.text)
                    match_id = match_link.split("/")[2]
                    playing_teams = match_title.split(",")[0].split(" vs ")
                    match_object = Match(match_id, match_title, match_format,
                                         playing_teams, match_venue.text,
                                         match_status, Common.home_page + match_link)
                    self.matches_list.append(match_object)

    def __init__(self, series_id, series_title, series_year, series_link):
        self.series_id = series_id
        self.series_title = series_title
        self.series_year = series_year
        self.series_link = series_link
        self.matches_list = []
        self.__extract_matches_list_of_series()

    def get_matches_list(self):
        return self.matches_list


class CalenderYear:
    def __extract_series_list_in_calender_year(self):
        link = Common.home_page + "/cricket-scorecard-archives/" + str(self.year)
        soup = Common.get_soup_object(link)
        series_blocks = soup.find_all('a', class_='text-hvr-underline')
        for series_block in series_blocks:
            series_link = series_block.get('href')
            if "cricket-series" in series_link:
                series_id = series_link.split("/")[2]
                series_title = series_block.text.split(",")[0]
                series_link = Common.home_page + series_link
                series_object = Series(series_id, series_title, self.year, series_link)
                self.series_list.append(series_object)

    def __init__(self, year):
        self.year = year
        self.series_list = []
        self.__extract_series_list_in_calender_year()

    def get_series_list(self):
        return self.series_list


calender = CalenderYear(2018)

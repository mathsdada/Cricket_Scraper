import requests
from bs4 import BeautifulSoup
import threading
from difflib import SequenceMatcher
import logging
from datetime import datetime
from pytz import timezone


class Common:
    home_page = "https://www.cricbuzz.com"
    match_formats = ["T20", "ODI", "TEST"]
    ball_outcome_mapping = {
        # Please do not change this order. It will cause regression..
        "out ": {'runs': 0, 'balls': 1, 'wicket': True, 'no_ball': False},
        "no ball": {'runs': 0, 'balls': 1, 'wicket': False, 'no_ball': True},
        "wide": {'runs': 0, 'balls': 0, 'wicket': False, 'no_ball': False},
        "byes": {'runs': 0, 'balls': 1, 'wicket': False, 'no_ball': False},
        "SIX": {'runs': 6, 'balls': 1, 'wicket': False, 'no_ball': False},
        "FOUR": {'runs': 4, 'balls': 1, 'wicket': False, 'no_ball': False},
        "1 run": {'runs': 1, 'balls': 1, 'wicket': False, 'no_ball': False},
        "2 runs": {'runs': 2, 'balls': 1, 'wicket': False, 'no_ball': False},
        "3 runs": {'runs': 3, 'balls': 1, 'wicket': False, 'no_ball': False},
        "no run": {'runs': 0, 'balls': 1, 'wicket': False, 'no_ball': False},
    }

    @staticmethod
    def replace_team_name(team_name):
        return {
            "West Indies": "Windies",
            "UAE": "United Arab Emirates",
            "HK": "Hong Kong",
            "Marylebone Cricket Club World XI": "MCC World XI",
            "Pakistan U-19": "Pakistan U19",
            "West Indies Women": "Windies Women",
            "Rising Pune Supergiants": "Rising Pune Supergiant",
            "St Lucia Zouks": "St Lucia Stars",
            "Cobras": "Cape Cobras",
            "West Indies U19": "Windies U19",
            "West Indies A": "Windies A",
            "Trinidad & Tobago": "Trinidad and Tobago",
            "Wayamba": "Wayamba Elevens",
            "RSA": "South Africa",
            "SL": "Sri Lanka"
        }.get(team_name, team_name)

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
        if ("practice" in match_type) or ("warm-up" in match_type) or ("unofficial" in match_type):
            return None
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
            return None

    @staticmethod
    def get_match_outcome(match_outcome):
        result_pattern = ["match tied", " won by ", "match drawn", " abandoned", "no result"]
        result_type = ["TIE", "WIN", "DRAW", "NO RESULT", "NO RESULT"]
        match_outcome = match_outcome.lower()
        for index, pattern in enumerate(result_pattern):
            if pattern in match_outcome:
                return result_type[index]
        return None

    @staticmethod
    def get_match_winning_team(match_status, match_result):
        if match_status == "WIN":
            if " won by " in match_result:
                match_winner = match_result.split(" won by ")[0]
            else:
                match_winner = match_result.split(" Won by ")[0]
        else:
            match_winner = "--"
        return Common.replace_team_name(match_winner.strip())

    @staticmethod
    def is_series_valid(series_link):
        ignore_list = ["qualifier", "warm-up", "practice"]
        for item in ignore_list:
            if item in series_link:
                return False
        return True

    @staticmethod
    def correct_player_name(name):
        name = name.strip().split("(c)")[0].split("(wk)")[0].split("(c & wk)")[0].strip()
        if name.endswith(" sub"):
            name = name.replace(" sub", "")
        elif name.endswith(" Sub"):
            name = name.replace(" Sub", "")
        return name

    @staticmethod
    def get_close_match(name, target_list):
        max_matching_size = -1
        result = ""
        for target in target_list:
            s = SequenceMatcher(None, name, target)
            cur_matching_size = 0
            for match_block in s.get_matching_blocks():
                cur_matching_size = max(cur_matching_size, match_block.size)
            if cur_matching_size > max_matching_size:
                max_matching_size = cur_matching_size
                result = target
        logging.getLogger(__name__).info(" {} {}: {}".format(threading.current_thread().name, name, result))
        return result

    @staticmethod
    def get_date_now():
        # Apr 14, 2018, Saturday
        # refer this link for more info. https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
        now = datetime.now()
        return now.strftime("%b %d, %Y, %A")

    @staticmethod
    def get_epoch_time_from_gmt(time):
        time_format = "%A, %B %d, %Y %I:%M %p %Z"
        time_zone = timezone('GMT')
        gmt_time = time_zone.localize(datetime.strptime(time, time_format))
        return int(gmt_time.timestamp())

    @staticmethod
    def get_id_from_link(link):
        return link.replace(Common.home_page, "").split("/")[2]
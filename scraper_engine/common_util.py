import requests
from bs4 import BeautifulSoup
import threading


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

    special_players = {
        "Andrew Balbirnie": "Andy Balbirnie",
        "Shardul Thakur":   "SN Thakur",
        "Cephas Zhuwao":    "Zhuwawo",
        "Rohit Paudel":     "Rohit Kumar",
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
    def get_short_names_of(name):
        # This function assumes maximum of 3 words in name.
        # Raise exception if name has more than 3 words
        names = [name]
        words = name.split()
        num_words = len(words)
        if num_words > 4:
            raise ValueError("Number of words in name(={}) are more than 3 . Detected by {}".format(
                name, threading.current_thread().name))
        for word in words:
            names.append(word)
        if num_words == 2:
            names.append(words[0][0].upper() + ' ' + words[1])
            # names.append(words[0] + ' ' + words[1][0].upper())
        if num_words == 3:
            names.append(words[0] + ' ' + words[1])
            names.append(words[0] + ' ' + words[2])
            names.append(words[1] + ' ' + words[2])
            names.append(words[0][0].upper() + ' ' + words[1])
            names.append(words[0][0].upper() + ' ' + words[2])
            names.append(words[1][0].upper() + ' ' + words[2])
            names.append(words[0][0].upper() + words[1][0].upper() + ' ' + words[2])
        if num_words == 4:
            # Roelof van der Merwe ==> van der Merwe
            # Timm van der Gugten ==> van der Gugten
            # Rassie van der Dussen ==> Dussen
            # ME Yazh Arun Mozhi ==> Yazh Arun Mozhi
            # Nicky van den Bergh ==> van den Bergh
            names.append(words[1] + ' ' + words[2] + ' ' + words[3])
        if name in Common.special_players:
            names.append(Common.special_players[name])
        return names

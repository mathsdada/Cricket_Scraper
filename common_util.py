import requests
from bs4 import BeautifulSoup


class Common:
    home_page = "http://www.cricbuzz.com"
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

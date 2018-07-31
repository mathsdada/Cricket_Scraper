import requests
from bs4 import BeautifulSoup
from Common import HeadToHead

ball_outcome_mapping = {
    "SIX": {'runs': 6, 'balls': 1, 'wicket': False, 'no_ball': False},
    "FOUR": {'runs': 4, 'balls': 1, 'wicket': False, 'no_ball': False},
    "1 run": {'runs': 1, 'balls': 1, 'wicket': False, 'no_ball': False},
    "2 runs": {'runs': 2, 'balls': 1, 'wicket': False, 'no_ball': False},
    "3 runs": {'runs': 3, 'balls': 1, 'wicket': False, 'no_ball': False},
    "no run": {'runs': 0, 'balls': 1, 'wicket': False, 'no_ball': False},
    "wide": {'runs': 0, 'balls': 0, 'wicket': False, 'no_ball': False},
    "no ball": {'runs': 0, 'balls': 1, 'wicket': False, 'no_ball': True},
    "leg byes": {'runs': 0, 'balls': 1, 'wicket': False, 'no_ball': False},
    "out ": {'runs': 0, 'balls': 1, 'wicket': True, 'no_ball': False},
}


class Commentary:
    def __init__(self, link):
        self.link = link
        self.html = requests.get(link).text
        self.commentary_data = []
        self.head_to_head_object_cache = {}
        soup = BeautifulSoup(self.html, 'lxml')
        commentary_blocks = soup.find_all('p', class_='cb-col cb-col-90 cb-com-ln')
        for commentary_block in reversed(commentary_blocks):
            ball_commentary = commentary_block.text.split(',')
            self.commentary_data.append(ball_commentary)

    def __get_head_to_head_object(self, batsman, bowler):
        if batsman in self.head_to_head_object_cache:
            if bowler not in self.head_to_head_object_cache[batsman]:
                self.head_to_head_object_cache[batsman][bowler] = HeadToHead(batsman, bowler)
        else:
            self.head_to_head_object_cache[batsman] = {}
            self.head_to_head_object_cache[batsman][bowler] = HeadToHead(batsman, bowler)
        return self.head_to_head_object_cache[batsman].get(bowler)

    def __get_outcome_of_a_ball(self, ball_outcome_str, ball_outcome_str_extra):
        outcome = None
        ball_data_string = ball_outcome_str.strip()
        ball_data_string_extra = ball_outcome_str_extra.strip()
        for item in ball_outcome_mapping:
            if item in ball_data_string:
                outcome = ball_outcome_mapping[item].copy()
                break
        if outcome['no_ball']:
            outcome_extra = self.__get_outcome_of_a_ball(ball_data_string_extra, "")
            outcome['runs'] = outcome_extra['runs']
        return outcome

    def get_head_to_head_data(self):
        head_to_head_data = []
        for ball_commentary in self.commentary_data:
            players = ball_commentary[0].split(" to ")
            print([ball_commentary[1], ball_commentary[2]])
            batsman = players[1].strip()
            bowler = players[0].strip()
            head_to_head = self.__get_head_to_head_object(batsman, bowler)

        # Get list of head_to_head objects of this match
        for batsman in self.head_to_head_object_cache:
            for bowler in self.head_to_head_object_cache[batsman]:
                head_to_head_data.append(self.head_to_head_object_cache[batsman][bowler])
        return head_to_head_data


commentary = Commentary("https://www.cricbuzz.com/cricket-scores/20084/rcb-vs-csk-24th-match-indian-premier-league-2018")
data = commentary.get_head_to_head_data()
print("Hello")

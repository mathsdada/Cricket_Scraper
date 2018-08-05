import requests
from bs4 import BeautifulSoup

from common_util import Common
from model.head_to_head import HeadToHead


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
        outcome = {'runs': 0, 'balls': 0, 'wicket': False, 'no_ball': False}
        ball_data_string = ball_outcome_str.strip()
        ball_data_string_extra = ball_outcome_str_extra.strip()
        for item in Common.ball_outcome_mapping:
            if item in ball_data_string:
                outcome = Common.ball_outcome_mapping[item].copy()
                break
        if outcome['no_ball']:
            outcome_extra = self.__get_outcome_of_a_ball(ball_data_string_extra, "")
            outcome['runs'] = outcome_extra['runs']
        if outcome['wicket'] and ("Run Out!!" in ball_data_string):
            # get number of runs taken before getting out for Run Out!!
            #  out de Grandhomme Run Out!! de Grandhomme isn't the quickest between the wickets.
            #  out Negi Run Out!! 1 run completed.
            outcome['wicket'] = False
            if " completed." in ball_data_string:
                outcome_extra = self.__get_outcome_of_a_ball(
                    ball_data_string.split("Run Out!!")[1].split(" completed.")[0].strip(), "")
                outcome['runs'] = outcome_extra['runs']
        return outcome

    def get_head_to_head_data(self):
        head_to_head_data = []
        for ball_commentary in self.commentary_data:
            players = ball_commentary[0].split(" to ")
            if len(players) < 2:
                print([ball_commentary, self.link])
                continue
            batsman = players[1].strip()
            bowler = players[0].strip()
            head_to_head = self.__get_head_to_head_object(batsman, bowler)
            if len(ball_commentary) >= 3:
                outcome = self.__get_outcome_of_a_ball(ball_commentary[1], ball_commentary[2])
            elif len(ball_commentary) >= 2:
                outcome = self.__get_outcome_of_a_ball(ball_commentary[1], "")
            else:
                print([ball_commentary, self.link])
                continue
            head_to_head.add_score(outcome['balls'], outcome['runs'], outcome['wicket'])
        # Get list of head_to_head objects of this match
        for batsman in self.head_to_head_object_cache:
            for bowler in self.head_to_head_object_cache[batsman]:
                head_to_head_data.append(self.head_to_head_object_cache[batsman][bowler])
        return head_to_head_data
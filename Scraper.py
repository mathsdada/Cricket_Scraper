import requests
from bs4 import BeautifulSoup
from Common import HeadToHead


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

    def get_head_to_head_data(self):
        head_to_head_data = []
        for ball_commentary in self.commentary_data:
            players = ball_commentary[0].split(" to ")
            batsman = players[1].strip()
            bowler = players[0].strip()
            head_to_head = self.__get_head_to_head_object(batsman, bowler)

        # Get list of head_to_head objects of this match
        for batsman in self.head_to_head_object_cache:
            for bowler in self.head_to_head_object_cache[batsman]:
                head_to_head_data.append(self.head_to_head_object_cache[batsman][bowler])
        return head_to_head_data


commentary = Commentary("https://www.cricbuzz.com/cricket-scores/20096/srh-vs-dd-36th-match-indian-premier-league-2018")
data = commentary.get_head_to_head_data()
print("Hello")

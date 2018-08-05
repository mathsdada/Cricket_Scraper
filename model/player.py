from common_util import Common


class Player:
    def __init__(self, name, player_id):
        self.name = name
        self.player_id = player_id
        self.role = '--'
        self.batting_style = '--'
        self.bowling_style = '--'
        self.__extract_player_profile()

    def __extract_player_profile(self):
        default_player_profile = {'Role': '--', 'Batting Style': '--', 'Bowling Style': '--'}
        default_keys = default_player_profile.keys()
        player_link = "http://www.cricbuzz.com/profiles/" + str(self.player_id)
        soup = Common.get_soup_object(player_link)
        key_tags = soup.findAll('div', class_="cb-col cb-col-40 text-bold cb-lst-itm-sm")
        value_tags = soup.findAll('div', "cb-col cb-col-60 cb-lst-itm-sm")
        for key, val in zip(key_tags, value_tags):
            key = key.text.strip()
            if key in default_keys:
                default_player_profile[key] = val.text.strip()
        self.role = default_player_profile['Role']
        self.batting_style = default_player_profile['Batting Style']
        self.bowling_style = default_player_profile['Bowling Style']

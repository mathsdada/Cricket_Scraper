from scraper.common_util import Common


class Player:
    def __init__(self, name, player_id):
        self.__name = name
        self.__id = player_id
        self.__role = '--'
        self.__batting_style = '--'
        self.__bowling_style = '--'
        self.__extract_player_profile()

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__id

    def get_role(self):
        return self.__role

    def get_batting_style(self):
        return self.__batting_style

    def get_bowling_style(self):
        return self.__bowling_style

    def __extract_player_profile(self):
        default_player_profile = {'Role': '--', 'Batting Style': '--', 'Bowling Style': '--'}
        default_keys = default_player_profile.keys()
        player_link = "http://www.cricbuzz.com/profiles/" + str(self.__id)
        soup = Common.get_soup_object(player_link)
        key_tags = soup.find_all('div', class_="cb-col cb-col-40 text-bold cb-lst-itm-sm")
        value_tags = soup.find_all('div', "cb-col cb-col-60 cb-lst-itm-sm")
        for key, val in zip(key_tags, value_tags):
            key = key.text.strip()
            if key in default_keys:
                default_player_profile[key] = val.text.strip()
        self.__role = default_player_profile['Role']
        self.__batting_style = default_player_profile['Batting Style']
        self.__bowling_style = default_player_profile['Bowling Style']

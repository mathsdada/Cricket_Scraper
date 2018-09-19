from scraper.common_util import Common
from scraper.model.schedule.series import Series
from scraper.model.player import Player


class Match:
    def __init__(self, title, venue, link, series_object):
        self.id = Common.get_id_from_link(link)
        self.title = title
        self.venue = venue
        # teams is a dictionary in below form
        # {'team-1' : [team-1's squad], 'team-2' : [team-2's squad]}
        self.teams = {}
        self.format = None
        self.time = None

        self.is_valid = False
        self.series = series_object
        self.link = link
        self.match_info = {}

        playing_teams = title.split(",")[0].split(" vs ")
        self.teams[playing_teams[0]] = {'short_name': playing_teams[0], 'squad': []}
        self.teams[playing_teams[1]] = {'short_name': playing_teams[1], 'squad': []}

        self.__extract_match_data()

    def __extract_match_data(self):
        link = self.link.replace("live-cricket-scores", "live-cricket-scorecard")
        soup = Common.get_soup_object(link)
        if self.series is None:
            self.series = self.__extract_series_object(soup)
        self.format = Common.get_match_format(self.title, self.series.format)
        if self.format is not None:
            self.__extract_match_info(soup)
            if self.__is_valid() is True:
                self.__extract_teams(soup)
                self.__extract_teams_short_names()
                self.time = self.__get_match_time()
                self.is_valid = True

    def __extract_series_object(self, soup):
        series_block = soup.find('div', class_='cb-nav-subhdr cb-font-12').find('a', href=True)
        series_title = series_block.text
        series_link = Common.home_page + series_block.get('href')

        return Series(series_title, series_link)

    def __extract_team_squad(self, squad_block):
        squad = []
        player_blocks = squad_block.find_all('a', class_='margin0 text-black text-hvr-underline')
        for player_block in player_blocks:
            player_id = player_block.get('href').split("/")[2]
            player_name = player_block.text
            player_name = Common.correct_player_name(player_name)
            squad.append(Player(player_name, player_id))
        return squad

    def __extract_teams(self, soup):
        squad_blocks = soup.find_all('div', 'cb-col cb-col-100 cb-minfo-tm-nm')
        if len(squad_blocks) == 3:
            team_a = squad_blocks[0].text.split('\xa0')[0].strip()
            team_b = soup.find('div', 'cb-col cb-col-100 cb-minfo-tm-nm cb-minfo-tm2-nm').text \
                .split('\xa0')[0].strip()
            team_a_squad_block = squad_blocks[1]
            team_b_squad_block = squad_blocks[2]
            if team_a in self.teams and team_b in self.teams:
                self.teams[team_a]['squad'] = self.__extract_team_squad(team_a_squad_block)
                self.teams[team_b]['squad'] = self.__extract_team_squad(team_b_squad_block)
            else:
                raise Exception("Squad Error....[{}, {}] {}".format(team_a, team_b, list(self.teams.keys())))

    def __extract_match_info(self, soup):
        match_info_items = soup.find_all('div', class_='cb-col cb-col-100 cb-mtch-info-itm')
        for match_info_item in match_info_items:
            key = match_info_item.find('div', class_='cb-col cb-col-27').text.strip()
            value = match_info_item.find('div', class_='cb-col cb-col-73').text.strip()
            self.match_info[key] = value

    def __get_match_time(self):
        date = self.match_info['Date'].split(" - ")[0].strip()
        time = self.match_info['Time']
        return Common.get_epoch_time_from_gmt(date + ' ' + time)

    def __extract_teams_short_names(self):
        full_names = self.title.split(",")[0].split(" vs ")
        short_names = self.match_info['Match'].split(",")[0].split(" vs ")
        self.teams[full_names[0]]['short_name'] = short_names[0]
        self.teams[full_names[1]]['short_name'] = short_names[1]

    def get_series_object(self):
        return self.series

    def __is_valid(self):
        if 'Toss' in self.match_info:
            return False
        return True

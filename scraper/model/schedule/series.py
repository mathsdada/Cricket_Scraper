from scraper.common_util import Common


class Series:
    def __init__(self, title, link):
        self.title = title
        self.format = []

        self.link = link
        self.matches_list = []
        self.__extract_series_info()

    def __extract_series_info(self):
        soup = Common.get_soup_object(self.link)
        self.format = soup.find('div', class_='cb-col-100 cb-col cb-nav-main cb-bg-white')\
                           .find('div').text.split(".")[0]

    def add_match(self, match):
        self.matches_list.append(match)

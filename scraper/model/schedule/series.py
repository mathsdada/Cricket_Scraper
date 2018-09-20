from scraper.common_util import Common


class Series:
    def __init__(self, title, link, category):
        self.title = title
        self.id = Common.get_id_from_link(link)
        self.gender = "Men"
        self.category = category
        if "women" in title.lower():
            self.gender = "Women"

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

    def get_matches_list(self):
        return self.matches_list

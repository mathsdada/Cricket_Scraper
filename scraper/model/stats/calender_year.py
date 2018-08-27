from scraper.common_util import Common
from scraper.model.stats.series import Series


class CalenderYear:
    def __init__(self, year):
        self.year = year
        self.series_list = []
        self.__extract_series_list_in_calender_year()

    def get_series_list(self):
        return self.series_list

    def __extract_series_list_in_calender_year(self):
        link = Common.home_page + "/cricket-scorecard-archives/" + str(self.year)
        soup = Common.get_soup_object(link)
        series_blocks = soup.find_all('a', class_='text-hvr-underline')
        for index, series_block in enumerate(series_blocks):
            series_link = series_block.get('href')
            if ("cricket-series" in series_link) and Common.is_series_valid(series_link):
                series_id = series_link.split("/")[2]
                series_title = series_block.text  # .split(",")[0]
                series_link = Common.home_page + series_link
                series_object = Series(series_id, series_title, self.year, series_link)
                self.series_list.append(series_object)

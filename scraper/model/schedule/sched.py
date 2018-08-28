from scraper.common_util import Common


class Schedule:
    def __init__(self, date):
        self.date = date
        self.series_list = []
        self.__get_schedule()

    def __get_schedule(self):
        soup = Common.get_soup_object("https://www.cricbuzz.com/cricket-schedule/upcoming-series/")
        category_blocks = soup.find_all('div', {'class': 'cb-col-100 cb-col', 'ng-show': True})
        for category_block in category_blocks:
            if category_block.next_element.text == self.date:
                series_blocks = category_block.find_all('div', class_='cb-col-100 cb-col')
                for series_block in series_blocks:
                    print(series_block.next_element.text)
from scraper.common_util import Common


class Schedule:
    def __init__(self, date):
        self.date = date
        self.series_list = []
        self.__get_schedule()

    def __get_schedule(self):
        soup = Common.get_soup_object("https://www.cricbuzz.com/cricket-schedule/upcoming-series/")
        date_blocks = soup.find_all('div', {'class': 'cb-col-100 cb-col', 'ng-show': True})
        for date_block in date_blocks:
            if date_block.next_element.text == self.date:
                print(date_block.next_element.text)
from scraper.common_util import Common
from scraper.model.schedule.match import Match


class Schedule:
    def __init__(self, date):
        self.date = date
        # {'series-1' : series-1's object, 'series-2' : series-2's object .....}
        self.series_data = {}
        self.__extract_schedule()

    def __extract_schedule(self):
        soup = Common.get_soup_object("https://www.cricbuzz.com/cricket-schedule/upcoming-series/")
        category_blocks = soup.find_all('div', {'class': 'cb-col-100 cb-col', 'ng-show': True})
        for category_block in category_blocks:
            if category_block.next_element.text == self.date:
                category_type = Common.get_category_type(category_block.get('ng-show'))
                series_blocks = category_block.find_all('div', class_='cb-col-100 cb-col')
                for series_block in series_blocks:
                    series_title = series_block.next_element.text
                    series_object = None
                    if series_title in self.series_data:
                        series_object = self.series_data[series_title]
                    match_blocks = series_block.find_all('div', 'cb-ovr-flo cb-col-60 cb-col cb-mtchs-dy-vnu ')
                    if (match_blocks is None) or\
                            ((match_blocks is not None) and (len(match_blocks) == 0)):
                        # Control comes here in case of multiple matches being played in single day of a series
                        match_blocks = series_block.find_all('div',
                                                             'cb-ovr-flo cb-col-60 cb-col cb-mtchs-dy-vnu cb-adjst-lst')
                    for match_block in match_blocks:
                        match_title_block = match_block.find('a', href=True)
                        match_title = match_title_block.text
                        match_link = Common.home_page + match_title_block.get('href')
                        match_venue = match_block.find('div').text

                        match_object = Match(match_title, match_venue, match_link, series_object, category_type)
                        if match_object.is_valid:
                            if series_object is None:
                                series_object = match_object.get_series_object()
                                self.series_data[series_title] = series_object
                            series_object.add_match(match_object)

    def get_list_of_series(self):
        series_list = []
        for key in self.series_data:
            series_list.append(self.series_data[key])
        return series_list

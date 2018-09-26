from database.database_engine import Database
from scraper.common_util import Common
from scraper.model.stats.match import Match
from database.schema.match import Match as match_db
import logging
import threading


class Series:
    def __init__(self, series_id, series_title, series_year, series_link):
        self.__id = series_id
        self.__title = series_title
        self.__year = series_year
        self.__gender = "Men"
        if "women" in series_title.lower():
            self.__gender = "Women"

        self.__series_link = series_link
        self.__db_match_table = None
        self.__matches_list = []
        self.__series_squad_ref = {}
        self.__logger = logging.getLogger(__name__)

    def extract_series_data(self):
        self.__logger.info("extract_series_data: thread={}, series={}".format(
            threading.current_thread().name, self.__title))
        database = Database()
        database.connect()
        self.__db_match_table = match_db(database.cursor)
        self.__extract_matches_list_of_series()
        database.close()

    def get_matches_list(self):
        return self.__matches_list

    def get_series_squad_ref(self):
        return self.__series_squad_ref

    def get_series_id(self):
        return self.__id

    def get_series_title(self):
        return self.__title

    def get_series_year(self):
        return self.__year

    def get_series_gender(self):
        return self.__gender

    def __extract_matches_list_of_series(self):
        soup = Common.get_soup_object(self.__series_link)
        series_formats = \
            soup.find('div', class_='cb-col-100 cb-col cb-nav-main cb-bg-white').find('div').text.split(".")[0]
        match_info_elements = soup.find_all('div', class_='cb-col-60 cb-col cb-srs-mtchs-tm')
        for match_info_element in match_info_elements:
            match_title_tag = match_info_element.find('a', class_='text-hvr-underline')
            match_venue_tag = match_info_element.find('div')
            [match_outcome_text, match_outcome] = self.__extract_match_outcome(
                match_info_element.find('a', class_='cb-text-link'))
            [is_valid_match, match_id, match_link, match_format] = self.__validate_match(
                match_title_tag, match_venue_tag, match_outcome, series_formats)
            if is_valid_match:
                [match_winning_team, win_margin] = Common.get_match_winning_team_and_margin(
                    match_outcome, match_outcome_text)
                match_object = Match(match_id, match_title_tag.text, match_format,
                                     match_venue_tag.text,
                                     match_outcome, Common.home_page + match_link, match_winning_team, win_margin)
                self.__matches_list.append(match_object)

    def __extract_match_outcome(self, match_outcome_block):
        if match_outcome_block is not None:
            match_outcome = Common.get_match_outcome(match_outcome_block.text)
        else:
            match_outcome = None
        return [match_outcome_block.text, match_outcome]

    def __validate_match(self, match_title_block, match_venue_block, match_outcome, series_formats):
        is_valid = False
        match_format = None
        match_id = None
        match_link = None
        if (match_title_block is not None) and ("cricket-scores" in match_title_block.get('href')) and \
                    (match_venue_block is not None) and (match_outcome is not None):
            match_format = Common.get_match_format(match_title_block.text, series_formats)
            if match_format is not None:
                match_link = match_title_block.get('href')
                match_id = match_link.split("/")[2]
                if self.__db_match_table.check_match_id(match_id):
                    self.__logger.info("Skipping {}. Available in DB".format(match_id))
                else:
                    is_valid = True
        return [is_valid, match_id, match_link, match_format]
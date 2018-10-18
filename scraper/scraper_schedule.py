from scraper.common_util import Common
from scraper.model.schedule.sched import Schedule


# filtered_category : 0 - International, 1 - Domestic & others, 2 - T20 Leagues
#                     3 - Women          9 - All Matches

class ScheduleScraper:
    def __init__(self):
        pass

    def get_schedule(self):
        now = Common.get_date_now()
        sched = Schedule(now)
        return sched.get_list_of_series()

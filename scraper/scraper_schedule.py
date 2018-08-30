from scraper.common_util import Common
from scraper.model.schedule.sched import Schedule


class ScheduleScraper:
    def __init__(self):
        pass

    def get_schedule(self):
        now = Common.get_date_now()
        sched = Schedule(now)
        return sched.get_list_of_series()

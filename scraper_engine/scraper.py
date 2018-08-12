from queue import Queue
from threading import Thread
import threading
from scraper_engine.model.calender_year import CalenderYear
import logging.config
import os


class Scraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.calender = None

    def get_data(self, year):
        self.calender = CalenderYear(year)
        self.__get_series_data()
        return self.calender

    def __get_series_data(self):
        num_series_threads = 8
        series_queue = Queue(maxsize=0)
        series_workers = []

        for series in self.calender.get_series_list():
            series_queue.put(series)
        for i in range(num_series_threads):
            series_worker = Thread(target=extract_series_data, args=(series_queue,))
            series_worker.setDaemon(True)
            series_worker.start()
            series_workers.append(series_worker)
        series_queue.join()
        for series_worker in series_workers:
            series_worker.join()


def extract_series_data(series_queue):
    while not series_queue.empty():
        series_object = series_queue.get()
        series_queue.task_done()
        series_object.extract_series_data()
        for match_object in series_object.get_matches_list():
            match_object.extract_match_data(series_object.squad)

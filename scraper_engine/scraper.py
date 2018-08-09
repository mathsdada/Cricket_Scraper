from queue import Queue
from threading import Thread
import threading
from scraper_engine.model.calender_year import CalenderYear


class Scraper:
    def __init__(self):
        pass

    def get_data(self, year):
        self.__get_data(year)
        return self.calender

    def __get_data(self, year):
        self.calender = CalenderYear(2018)
        self.__get_series_data()
        self.__get_match_data()

    def __get_series_data(self):
        num_series_threads = 8
        series_queue = Queue(maxsize=0)
        series_workers = []

        for series in self.calender.get_series_list():
            series_queue.put(series)
            # TODO Remove This
            break
        for i in range(num_series_threads):
            series_worker = Thread(target=extract_series_data, args=(series_queue,))
            series_worker.setDaemon(True)
            series_worker.start()
            series_workers.append(series_worker)
        series_queue.join()
        for series_worker in series_workers:
            series_worker.join()

    def __get_match_data(self):
        num_match_threads = 8
        match_queue = Queue(maxsize=0)
        match_workers = []

        for series in self.calender.get_series_list():
            for match in series.get_matches_list():
                match_queue.put([match, series])

        for i in range(num_match_threads):
            match_worker = Thread(target=extract_match_data, args=(match_queue,))
            match_worker.setDaemon(True)
            match_worker.start()
            match_workers.append(match_worker)
        match_queue.join()
        for match_worker in match_workers:
            match_worker.join()


def extract_series_data(series_queue):
    while not series_queue.empty():
        series_object = series_queue.get()
        print("extract_series_data: thread={}, depth={}, series={}".format(
            threading.current_thread().name, series_queue.qsize(), series_object.series_title))
        series_queue.task_done()
        series_object.extract_series_data()


def extract_match_data(match_queue):
    while not match_queue.empty():
        [match_object, series_object] = match_queue.get()
        print("extract_match_data: thread={}, depth={}, match={}".format(
            threading.current_thread().name, match_queue.qsize(), match_object.title))
        match_queue.task_done()
        match_object.extract_match_data(series_object.squad)


# scraper = Scraper()
# scraper.get_data(2018)
# print("Hellowwwww")
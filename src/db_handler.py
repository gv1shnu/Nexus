import os
import time
from tinydb import TinyDB, Query
from src.scrape import Scrape
from datetime import date


class DBHandler:
    def __init__(self):
        """
        Initializes the DBHandler object.
        Creates TinyDB instance for the search results database.
        """
        if not os.path.exists('db'):
            os.mkdir('db')
        self.db = TinyDB('db/search_results_db.json')

    @staticmethod
    def pagify(results: list) -> list:
        return results  # working here

    @staticmethod
    def retrieve(req: str) -> dict:
        scrape = Scrape(req)
        raw_results = scrape.get_results()
        results = DBHandler.pagify(raw_results)
        counter = scrape.get_counter()
        timer = scrape.get_timer()
        return {'query': req,
                'count': counter,
                'time': timer,
                'date': str(date.today()),
                'results': results
                }

    def insert(self, req: str) -> tuple:
        """
        Inserts a new entry into the search results database.
        Takes a request as input and driver service as pass-along parameter and
         performs web scraping if not stored, to obtain the search results.
        """
        if req:
            ans = self.retrieve(req)
            self.db.insert(ans)
            return ans['count'], ans['time'], ans['results']
        print("\033[95m Null request")

    def update(self, entry: dict) -> tuple:
        """
        Updates an old entry into the search results database.
        Takes a request as input and driver service as pass-along parameter and
         performs web scraping to obtain the new search results.
        """
        if entry:
            req = entry['query']
            ans = self.retrieve(req)
            id = Query()['query'] == req
            self.db.update(ans, id)
            return ans['count'], ans['time'], ans['results']
        print("\033[95m Null request")

    def query(self, req: str) -> dict:
        """
        Queries the search results database for a specific request.
        """
        id = Query()['query'] == req
        query_result = self.db.search(id)
        if query_result:
            print("Entry exists")
            return query_result[0]
        return {}

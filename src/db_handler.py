import os

import selenium.webdriver.chrome.service
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

    def insert(self, req: str, ds: selenium.webdriver.chrome.service.Service) -> list:
        """
        Inserts a new entry into the search results database.
        Takes a request as input and driver service as pass-along parameter and
         performs web scraping if not stored, to obtain the search results.
        """
        if req:
            scrape = Scrape(req, ds)
            results = scrape.get_results()
            ans = {'query': req,
                   'date': str(date.today()),
                   'results': results
                   }
            self.db.insert(ans)
            return results
        print("\033[95m Null request")
        return []

    def update(self, entry: list, ds: selenium.webdriver.chrome.service.Service) -> list:
        """
        Updates an old entry into the search results database.
        Takes a request as input and driver service as pass-along parameter and
         performs web scraping to obtain the new search results.
        """
        if entry:
            req = entry['query']
            scrape = Scrape(req, ds)
            results = scrape.get_results()
            ans = {'query': req,
                   'date': str(date.today()),
                   'results': results
                   }
            self.db.update(ans, Query().query == req)
            return ans['results']
        print("\033[95m Null request")
        return []

    def query(self, req: str) -> list:
        """
        Queries the search results database for a specific request.
        """
        query_result = self.db.search(Query().query == req)
        if query_result:
            print("Entry exists")
            return query_result[0]
        return []

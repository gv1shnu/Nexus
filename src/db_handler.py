import os
import time
from tinydb import TinyDB, Query
from src.scrape import Scrape
from datetime import date


def is_entry_old(entry_date: str) -> bool:
    """
    Checks if the entry date is older than a week.

    Args:
        entry_date (str): The date of the entry.

    Returns:
        bool: True if the entry is older than a week, False otherwise.
    """
    t1 = entry_date.split('-')
    t2 = str(date.today()).split('-')
    r = abs((int(t2[0]) - int(t1[0])) * 365 + (int(t2[1]) - int(t1[1])) * 12 + (int(t2[2]) - int(t1[2])))

    return r >= 7  # is older than a week


class DBHandler:
    def __init__(self):
        """
        Initializes the DBHandler object.
        Creates TinyDB instance for the search results database.
        """
        if not os.path.exists('db'):
            os.mkdir('db')
        self.db = TinyDB('db/search_results_db.json')
        self.items_per_page = 7

    def pagify(self, my_list: list) -> list:
        """
        Paginates a list of items into multiple pages.
        Returns a list of pages where each page contains a subset of og list.

        Parameters:
            my_list (list): complete list of cards

        Returns: list of pages
        """
        total_pages = len(my_list) // self.items_per_page + 1
        pages = []
        for page in range(total_pages):
            start_index = page * self.items_per_page
            end_index = start_index + self.items_per_page
            items = my_list[start_index:end_index]
            pages.append(items)
        return pages

    def retrieve(self, req: str) -> dict:
        """
        Retrieves search results for a given request.

        Returns a dictionary with query details including count, time,
        date, and paginated pages of results.

        Parameters:
        - req: The search request.

        Returns:
        - Dictionary with query details.
        """
        start_time = time.time()
        scrape = Scrape(req)
        results = scrape.get_all_results()
        pages = self.pagify(results)
        end_time = time.time()
        timer = round((end_time - start_time), 2)
        return {'query': req,
                'count': len(results),
                'time': timer,
                'date': str(date.today()),
                'pages': pages
                }

    def get(self, query: str) -> tuple:
        result = self.query(req=query)
        if result:  # entry exists
            if is_entry_old(entry_date=result['date']):
                return self.update(entry=result)
            else:  # is fresh
                return result['count'], result['time'], result['pages']
        else:
            return self.insert(req=query)

    def insert(self, req: str) -> tuple:
        """
        Inserts a new entry into the search results database.
        Takes a request as input and driver service as pass-along parameter and
         performs web scraping if not stored, to obtain the search results.

        Parameters:
        - req: The search request.

        Returns:
        - Tuple containing count, time, and paginated pages.
        """
        if req:
            print("\033[92m No entry found.\n Scraping...")
            ans = self.retrieve(req)
            self.db.insert(ans)
            print("\033[92mDone.")
            return ans['count'], ans['time'], ans['pages']
        print("\033[95m Null request")

    def update(self, entry: dict) -> tuple:
        """
        Updates an old entry into the search results database.
        Takes a request as input and driver service as pass-along parameter and
         performs web scraping to obtain the new search results.

        Parameters:
        - entry: The existing entry to update.

        Returns:
        - Tuple containing count, time, and paginated pages.
        """
        if entry:
            req = entry['query']
            ans = self.retrieve(req)
            id = Query()['query'] == req
            self.db.update(ans, id)
            return ans['count'], ans['time'], ans['pages']
        print("\033[95m Null request")

    def query(self, req: str) -> dict:
        """
        Queries the search results database for a specific request.

        Returns the matching entry if found, otherwise an empty dictionary.

        Parameters:
        - req: The search request.

        Returns:
        - The matching entry if found, otherwise an empty dictionary.
        """
        id = Query()['query'] == req
        query_result = self.db.search(id)
        if query_result:
            print("Entry exists")
            return query_result[0]
        return {}

import json
import os
import time
from tinydb import TinyDB, Query
from src.scrape import Scrape
from datetime import date, datetime


def is_entry_old(entry_date: str) -> bool:
    entry_date_obj = datetime.strptime(entry_date, '%Y-%m-%d').date()
    current_date = date.today()
    time_difference = current_date - entry_date_obj
    return time_difference.days >= 7  # is older than a week


class DBHandler:
    def __init__(self):
        os.makedirs('db', exist_ok=True)
        self.db_path = 'db/search_results.json'
        self.db = TinyDB(self.db_path)

    @staticmethod
    def pagify(my_list: list, items_per_page: int) -> list:
        total_pages = len(my_list) // items_per_page + 1
        pages = []
        for page in range(total_pages):
            start_index = page * items_per_page
            end_index = start_index + items_per_page
            items = my_list[start_index:end_index]
            pages.append(items)
        return pages

    def retrieve(self, req: str) -> dict:
        start_time = time.time()
        scrape = Scrape(req)
        results = scrape.get_all_results()
        pages = self.pagify(results, 7)
        end_time = time.time()
        timer = round((end_time - start_time), 2)
        current_time = datetime.now()
        return {'query': req,
                'count': len(results),
                'time': timer,
                'date': str(date.today()),
                'pages': pages,
                'timestamp': f"{current_time.hour}:{current_time.minute}"
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

    def get_queries(self) -> list:
        queries = []
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as file:
                try:
                    data = json.load(file)
                    data = data.get('_default', {})
                    queries = [{'date': item['date'], 'timestamp': item['timestamp'], 'query': item['query']}
                               for item in data.values()]
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
        return self.pagify(queries, 10)

    def insert(self, req: str) -> tuple:
        if req:
            print("\033[92m \nNo entry found.\n Scraping...")
            ans = self.retrieve(req)
            self.db.insert(ans)
            print("\033[92mDone.")
            return ans['count'], ans['time'], ans['pages']
        print("\033[95m \nNull request")

    def update(self, entry: dict) -> tuple:
        if entry:
            req = entry['query']
            ans = self.retrieve(req)
            entry_id = Query()['query'] == req
            self.db.update(ans, entry_id)
            return ans['count'], ans['time'], ans['pages']
        print("\033[95m \nNull request")

    def query(self, req: str) -> dict:
        entry_id = Query()['query'] == req
        query_result = self.db.search(entry_id)
        if query_result:
            print("\033[92m \nEntry exists")
            return query_result[0]
        return {}

    def clear(self):
        try:
            self.db.drop_tables()
            return True
        except Exception as e:
            print('Error clearing data:', e)
            return False


# Standard libraries
import os
from datetime import datetime
from typing import List, Dict

# Third-party libraries
from pytz import timezone
from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
from pymongo.cursor import Cursor

# Internal imports
from decl import Pages
from src.helpers import is_today
from utl.logger import Logger

logger = Logger()

username: str = quote_plus(str(os.environ.get('NEXUS_USERNAME', None)))
password: str = quote_plus(str(os.environ.get('NEXUS_PASSWORD', None)))
cluster: str = str(os.environ.get('NEXUS_CLUSTER', None))
URI: str = 'mongodb+srv://' + username + ':' + password + '@' + cluster + '/?retryWrites=true&w=majority'


class Handler:
    def __init__(self):
        self.client = MongoClient(URI)
        self.db = self.client['my_database']
        self.collection = self.db['my_collection']

    def insert(
            self, search_query: str, engines: List[str],
            _filter: str, count: int, results: Pages,
            scrape_time: float
    ):
        results_as_dict: List[List[Dict]] = [
            [card.to_dict() for card in inner_list]
            for inner_list in results
        ]
        search_record = {
            'search_query': search_query,
            'selected_engines': ",".join(engines),
            'filter': _filter,
            'count': count,
            'scrape_time': scrape_time,
            'timestamp': datetime.now(
                timezone("Asia/Kolkata")
            ).strftime('%Y-%m-%d %H:%M:%S.%f'),
            'results': results_as_dict
        }
        self.collection.insert_one(search_record)

    def get_search_history(self, search_query: str, engines: List[str] = None, _filter: str = None) -> List[Dict]:
        self.clear_history()
        search_history: Cursor = self.collection.find(
            {
                'search_query': search_query,
                'selected_engines': ",".join(engines),
                'filter': _filter
            }
        )
        return list(search_history)

    def clear_history(self):
        # Delete all history every day
        latest_entry: List[Dict] = list(self.collection.find().sort([('timestamp', -1)]).limit(1))
        if latest_entry:
            last_timestamp: str = latest_entry[0]['timestamp']
            if not is_today(last_timestamp):
                self.collection.delete_many({})
                logger.debug("Old entries cleared")

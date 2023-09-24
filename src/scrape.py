"""Scraping handler"""

import time
from typing import List, Callable

# Internal imports
from src.scr.google import get_google_results
from src.scr.ddg import get_ddg_results

# from src.scr.bing import get_bing_results
# from src.scr.yahoo import get_yahoo_results
# from src.scr.yt import get_yt_results
# from src.scr.reddit import get_reddit_results

from src.helpers import Card, remove_duplicate_cards, pagify
from utl.logger import Logger

logger = Logger()


class Scrape:
    def __init__(self):
        self.results = list()
        self.pairs = [
            # {'name': "bing", 'func': get_bing_results},  # 1
            {'name': "duckduckgo", 'func': get_ddg_results},  # 2
            # {'name': "yahoo", 'func': get_yahoo_results},  # 3
            # {'name': "youtube", 'func': get_yt_results},  # 4
            # {'name': "reddit", 'func': get_reddit_results},  # 5
            {'name': "google", 'func': get_google_results}  # 6
        ]

    def get_results(self, q_opt_f_tuple: tuple) -> List[List[Card]]:
        try:
            for pair in self.pairs:
                if pair['name'] in q_opt_f_tuple[1]:  # options
                    self._search(
                        q_opt_f_tuple[0],  # q
                        q_opt_f_tuple[2],  # filter
                        pair['func']
                    )
            return pagify(remove_duplicate_cards(self.results), 7)
        except Exception as e:
            logger.exception(f"An error occurred while getting all results: {e}")
            return []

    def _search(self, q: str, _filter: str, func: Callable):
        try:
            start = time.perf_counter()
            ans = func(q, _filter)
            end = time.perf_counter()
            timer = round((end - start), 2)
            self.results.extend(ans)
        except Exception as e:
            logger.exception(f"An error occurred while implementing search func: {e}")

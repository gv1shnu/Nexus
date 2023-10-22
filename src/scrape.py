"""Scraping handler"""

# Python standard libraries
import threading
from concurrent.futures import ThreadPoolExecutor
import time
from typing import List, Dict, Callable

# Internal imports
from src.helpers import remove_duplicate_cards, pagify
from src.scr.bs.yahoo import get_yahoo_results
from src.scr.sel.yt import get_yt_results
from utl.logger import Logger
from decl import Pages, ITEMS_PER_PAGE, Card

from src.scr.lib.ddg import get_ddg_results
from src.scr.lib.google import get_google_results


logger = Logger()


class Scrape:
    def __init__(self):
        self.results = list()
        self.pairs: List[Dict[str, Callable]] = [
            # {'name': "bing", 'func': get_bing_results},  # 1
            {'name': "duckduckgo", 'func': get_ddg_results},  # 2
            {'name': "yahoo", 'func': get_yahoo_results},  # 3
            # {'name': "youtube", 'func': get_yt_results},  # 4
            # {'name': "reddit", 'func': get_reddit_results},  # 5
            {'name': "google", 'func': get_google_results},  # 6
        ]
        self.results_lock = threading.Lock()

    def get_results(self, q_opt_f_tuple: tuple) -> Pages:
        try:
            start: float = time.perf_counter()
            with ThreadPoolExecutor(max_workers=len(self.pairs)) as executor:
                futures = list()
                for pair in self.pairs:
                    if pair['name'] in q_opt_f_tuple[1]:
                        future = executor.submit(
                            self._search,
                            q_opt_f_tuple[0],  # q
                            q_opt_f_tuple[2],  # filter
                            pair['func']
                        )
                        futures.append(future)
                for future in futures:
                    future.result()
            end: float = time.perf_counter()
            logger.info(f"all search took {round(end - start, 1)}s for {len(self.results)} results")

            return pagify(
                remove_duplicate_cards(
                    self.results
                ), ITEMS_PER_PAGE
            )
        except Exception as e:
            logger.exception(f"An error occurred while getting all results: {e}")
            return []

    def _search(self, q: str, _filter: str, func: Callable):
        try:
            _start: float = time.perf_counter()
            ans: List[Card] = func(q, _filter)
            with self.results_lock:
                self.results.extend(ans)
            _end: float = time.perf_counter()
            logger.info(f"{func.__name__} took {round(_end - _start, 1)}s for {len(ans)} results")
        except Exception as e:
            logger.exception(f"An error occurred while implementing search func: {e}")

import csv
import threading
import time
from scr.google import get_google_results
from scr.bing import get_bing_results
from scr.ddg import get_ddg_results
from scr.yahoo import get_yahoo_results
from scr.yt import get_yt_results


# Remove duplicate URLs
def preprocess(my_list: list) -> list:
    unique_urls = set()
    jkl = []
    for item in my_list:
        if item['url'] not in unique_urls:
            unique_urls.add(item['url'])
            jkl.append(item)
    return jkl


class Scrape:
    def __init__(self, q: str):
        """
        Initializes the Scrape object.

        Args:
            q (str): The search query.
        """
        self.query, self.results = q, []
        self.pairs = [
            {'name': "Bing", 'func': get_bing_results},
            {'name': "Duckduckgo", 'func': get_ddg_results},
            {'name': "Yahoo", 'func': get_yahoo_results},
            {'name': "YT", 'func': get_yt_results},
        ]  # google will run non-threaded

    def get_all_results(self) -> list:
        """
        Performs web scraping to obtain search results.
        Spawns multiple threads to scrape search results from different search engines concurrently.

        Returns:
            list: A list of dictionaries representing the search results.
        """
        threads = []
        for pair in self.pairs:
            thread = threading.Thread(target=self.search, args=(pair['name'], pair['func']))
            threads.append(thread)
        self.search("Google", get_google_results)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return preprocess(self.results)

    def search(self, name, func) -> None:
        """
        Search a specific engine with same query

        Args:
            name (str): The engine name
            func (function): The function to execute to scraper

        Returns: None
        """
        start = time.time()
        ans = func(self.query)
        end = time.time()
        timer = round((end - start), 2)
        print(f"{name} took {timer}s")
        self.save_stat(name, len(ans), timer)
        self.results.extend(ans)

    def save_stat(self, engine_name: str, count: int, timer: float) -> None:
        """
        Saves the search statistics to a CSV file.

        Args:
            engine_name (str): The name of the search engine.
            count (int): The number of results.
            timer (float): The time taken for the search.

        Returns:
            None
        """
        csv_file = 'db/stats.csv'
        field_names = ['query', 'engine', 'count', 'timer']

        with open(csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=field_names)

            # Check if the file is empty and write the header if needed
            if file.tell() == 0:
                writer.writeheader()

            writer.writerow({'query': self.query, 'engine': engine_name, 'count': count, 'timer': timer})

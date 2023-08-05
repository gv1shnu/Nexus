import threading
import time
import src.google as google
import src.ddg as ddg
import src.bing as bing
import src.yahoo as yahoo
import src.yt as yt


class Scrape:
    def __init__(self, q: str):
        """
        Initializes the Scrape object.

        Args:
            q (str): The search query.
        """
        self.query, self.counter, self.timer, self.results = q, {}, {}, []

    def get_counter(self) -> int:
        return sum(self.counter.values())

    def get_timer(self) -> int:
        return sum(self.timer.values())

    def get_results(self) -> list:
        """
        Performs web scraping to obtain search results.
        Spawns multiple threads to scrape search results from different search engines concurrently.

        Returns:
            list: A list of dictionaries representing the search results.
        """
        threads = [
            threading.Thread(target=self.get_bing_urls),
            threading.Thread(target=self.get_yahoo_urls),
            threading.Thread(target=self.get_duckduckgo_urls),
            threading.Thread(target=self.get_youtube_urls)
        ]
        self.get_google_urls()
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return self.results

    def get_google_urls(self) -> None:
        self.search('Google', google.get_res)

    def search(self, engine_name, func):
        """
        Search a specific engine with same query

        Args:
            engine_name (str): self-explanatory
            func: function to execute to store scraped results

        Returns: None
        """
        start_time = time.time()
        ans = func(self.query)
        end_time = time.time()
        self.counter[engine_name] = len(ans)
        self.timer[engine_name] = round((end_time - start_time), 2)
        self.results.append({
            'engine': engine_name,
            'count': self.counter[engine_name],
            'time': self.timer[engine_name],
            'results': ans
        })

    def get_bing_urls(self) -> None:
        self.search('Bing', bing.get_res)

    def get_yahoo_urls(self) -> None:
        self.search('Yahoo', yahoo.get_res)

    def get_duckduckgo_urls(self) -> None:
        self.search('Duckduckgo', ddg.get_res)

    def get_youtube_urls(self) -> None:
        self.search('YouTube', yt.get_res)

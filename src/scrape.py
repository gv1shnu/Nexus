import threading
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from googlesearch import search
from duckduckgo_search import DDGS
from urllib.parse import urlparse


def is_valid_url(url):
    """
    Checks if a URL is valid.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class Scrape:
    def __init__(self, q):
        """
        Initializes the Scrape object.

        Args:
            q (str): The search query.
        """
        self.query = q
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36'
        }
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless --no-sandbox --disable-dev-shm-usage --disable-gpu")
        self.driver_service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        self.results = []

    def get_results(self):
        """
        Performs web scraping to obtain search results.
        Spawns multiple threads to scrape search results from different search engines concurrently.

        Returns:
            list: A list of dictionaries representing the search results.
        """
        threads = [
            threading.Thread(target=self.get_google_urls),
            threading.Thread(target=self.get_bing_urls),
            threading.Thread(target=self.get_yahoo_urls),
            threading.Thread(target=self.get_duckduckgo_urls),
            threading.Thread(target=self.get_youtube_urls)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return self.results

    def get_google_urls(self):
        """
        Scrapes search results from Google.
        Uses the `search` function from the `googlesearch` library to perform the search.
        """
        ans = list()
        try:
            dip = search(self.query, advanced=True)
            for i in dip:
                unit = {'title': i.title, 'url': i.url, 'body': i.description}
                ans.append(unit)
            self.results.append({'engine': 'Google', 'results': ans})
        except Exception as e:
            print('\033[0mGoogle:', str(e))

    def get_bing_urls(self):
        """
        Scrapes search results from Bing.
        Sends a GET request to Bing with the query as a parameter.
        """
        base, t = "https://www.bing.com/", "search?q"
        url = f"{base}{t}={self.query}"
        try:
            response = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(response, 'html.parser')
            ans = list()
            data1 = soup.find('ol', id='b_results')
            if data1:
                data2 = data1.find_all("li")
                for li in data2:
                    unit = {'title': None, 'url': None, 'body': None}
                    h2_element = li.find('h2')
                    caption = li.find('div', class_="b_caption")
                    if h2_element:
                        anchor_tag = h2_element.find('a')
                        if anchor_tag:
                            if is_valid_url(anchor_tag['href']):
                                unit['title'], unit['url'] = h2_element.text, anchor_tag['href']
                    if caption:
                        p_tag = caption.find('p')
                        unit['body'] = p_tag.text[3:]

                    if unit['title'] and unit['url']:
                        ans.append(unit)
                self.results.append({'engine': 'Bing', 'results': list(ans)})
        except Exception as e:
            print('\033[0mBing:', str(e))
            print(url)

    def get_yahoo_urls(self):
        """
        Scrapes search results from Yahoo.
        Sends a GET request to Yahoo with the query as a parameter.
        """
        base_url = 'https://search.yahoo.com/search'
        params = {
            'q': self.query,
            'b': '0',  # (0 for the first page)
        }
        response = requests.get(base_url, params=params)
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            ans = list()
            result_container = soup.find('ol', class_='reg searchCenterMiddle')
            if result_container:
                for li in result_container.find_all('li'):
                    unit = {'title': None, 'url': None, 'body': None}
                    div = li.find('div', class_="compTitle options-toggle")
                    if div:
                        h3 = div.find('h3')
                        if h3:
                            anchor_tag = h3.find('a')
                            if anchor_tag:
                                unit['title'] = anchor_tag.get_text(strip=True)
                                if is_valid_url(anchor_tag['href']):
                                    unit['url'] = anchor_tag['href']
                    p_div = li.find('div', class_="compText aAbs")
                    if p_div:
                        p_element = p_div.find('p')
                        if p_element:
                            unit['body'] = p_element.find('span').text

                    if unit['title'] and unit['url']:
                        ans.append(unit)

            self.results.append({'engine': 'Yahoo', 'results': ans})
        except Exception as e:
            print('\033[0mYahoo:', str(e))
            print(response.url)

    def get_duckduckgo_urls(self):
        """
        Scrapes search results from DuckDuckGo.
        Uses the `DDGS` class from the `duckduckgo_search` library to perform the search.
        """
        ans = list()
        try:
            for r in DDGS().text(self.query):
                unit = {'title': r['title'], 'url': r['href'], 'body': r['body']}
                ans.append(unit)
            self.results.append({'engine': 'Duckduckgo', 'results': ans})
        except Exception as e:
            print('\033[0mDDG:', str(e))

    def get_youtube_urls(self):
        """
        Scrapes search results from YouTube.
        Uses Selenium WebDriver to simulate a browser and perform the search.
        """
        ans = list()
        base, t = "https://www.youtube.com/", "results?search_query"
        x = "+".join(self.query.split(' '))
        url = f"{base}{t}={x}"
        try:
            driver = webdriver.Chrome(service=self.driver_service, options=self.chrome_options)
            driver.get(url)
            common_path = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/"

            for _ in range(3):  # Scroll down three times to load more videos
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(2)

            for i in range(1, 21):
                f = common_path + f"ytd-video-renderer[{str(i)}]/div[1]/div/div[1]/div/h3/a"
                divs = driver.find_element("xpath", f)

                time.sleep(3)
                g = common_path + f"ytd-video-renderer[{str(i)}]/div[1]/div/div[3]/a/yt-formatted-string"
                t_divs = driver.find_element("xpath", g)

                unit = {'title': divs.text, 'url': divs.get_attribute('href'), 'body': t_divs.text}
                ans.append(unit)
            self.results.append({'engine': 'YouTube', 'results': ans})
        except Exception as e:
            print('\033[0mYT:', str(e))
            print(url)

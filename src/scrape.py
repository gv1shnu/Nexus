import random
import threading
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from duckduckgo_search import DDGS
from urllib.parse import urlparse
from selenium.webdriver.common.by import By


def is_valid_url(url) -> bool:
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


def get_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc


class Scrape:
    def __init__(self, q: str, ds):
        """
        Initializes the Scrape object.

        Args:
            q (str): The search query.
            ds (selenium.webdriver.chrome.service.Service): The pass along.
        """
        self.query = q
        self.headers = None
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.55 Safari/537.36'
        ]
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless --no-sandbox --disable-dev-shm-usage --disable-gpu")
        self.driver_service = ds
        self.assign_header()
        self.results = []

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
        """
        Scrapes search results from Google.
        """
        dips = search(self.query, advanced=True)
        ans = [{'title': dip.title, 'url': dip.url, 'channel_name': get_domain(dip.url),
                'channel_url': get_domain(dip.url), 'body': dip.description} for dip in dips]
        self.results.append({'engine': 'Google', 'results': ans})

    def get_bing_urls(self) -> None:
        """
        Scrapes search results from Bing.
        Sends a GET request to Bing with the query as a parameter.
        """
        url = self.get_url(base="https://www.bing.com/", t="search?q")
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
                        unit['channel_name'] = get_domain(unit['url'])
                        unit['channel_url'] = get_domain(unit['url'])
                        ans.append(unit)
            self.results.append({'engine': 'Bing', 'results': list(ans)})
        except NoSuchElementException:
            print('\033[0mBing. {}'.format(url))

    def get_yahoo_urls(self) -> None:
        """
        Scrapes search results from Yahoo.
        Sends a GET request to Yahoo with the query as a parameter.
        """
        base_url = self.get_url(base='https://search.yahoo.com/', t='search?q')
        response = requests.get(base_url, headers=self.headers)
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
                        unit['channel_name'] = get_domain(unit['title'])
                        unit['channel_url'] = get_domain(unit['title'])
                        ans.append(unit)

            self.results.append({'engine': 'Yahoo', 'results': ans})
        except NoSuchElementException:
            print('\033[0mYahoo. {}'.format(response.url))

    def get_duckduckgo_urls(self) -> None:
        """
        Scrapes search results from DuckDuckGo.
        """
        ans = [{'title': r['title'], 'url': r['href'], 'channel_name': get_domain(r['href']),
                'channel_url': get_domain(r['href']), 'body': r['body']} for r in DDGS().text(self.query)]
        self.results.append({'engine': 'Duckduckgo', 'results': ans})

    def get_youtube_urls(self) -> None:
        """
        Scrapes search results from YouTube.
        Uses Selenium WebDriver to simulate a browser and perform the search.
        """
        ans = list()
        url = self.get_url(base="https://www.youtube.com/", t="results?search_query")
        try:
            driver = webdriver.Chrome(service=self.driver_service, options=self.chrome_options)
            driver.get(url)
            elem = driver.find_element(By.ID, 'contents')
            children_elems = elem.find_elements(By.CSS_SELECTOR, 'ytd-video-renderer')  # blocks
            for child in children_elems:
                nested_child = child.find_element(By.ID, 'dismissible')
                yf = nested_child.find_elements(By.CSS_SELECTOR, "yt-formatted-string")
                body = ""
                for i in yf:
                    if 'metadata' in i.get_attribute('class'):
                        body += i.text
                video_url, video_title, channel_url, channel_name = "", "", "", ""
                yf_url = nested_child.find_elements(By.TAG_NAME, 'a')
                i = 0
                for k in yf_url:
                    if k.text:
                        i += 1
                        if i == 2:
                            channel_url = k.get_attribute('href')
                            channel_name = k.text
                        elif i == 1:
                            video_url = k.get_attribute('href')
                            video_title = k.text
                        else:
                            pass
                    else:
                        pass
                unit = {'title': video_title, 'url': video_url, 'body': body, 'channel_name': channel_name,
                        'channel_url': channel_url}
                ans.append(unit)
            self.results.append({'engine': 'YouTube', 'results': ans})
            driver.close()
        except NoSuchElementException:
            print('\033[0mYT: {}'.format(url))

    def get_url(self, base: str, t: str) -> str:
        x = "+".join(self.query.split(' '))
        return f"{base}{t}={x}"

    def assign_header(self) -> None:
        tmp = random.choice(self.user_agents)
        self.headers = {'User-Agent': tmp}

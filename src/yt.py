from src.helpers import get_url
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.driver import driver_service
from selenium.common import NoSuchElementException


chrome_options = Options()
chrome_options.add_argument("--headless --no-sandbox --disable-dev-shm-usage --disable-gpu")


def get_res(query: str) -> list:
    """
    Scrapes search results from YouTube.

    Args:
        query (str): the search query.

    Returns: a list of dictionaries
    """
    ans = list()
    url = get_url(q=query, base="https://www.youtube.com/", t="results?search_query")
    try:
        driver = webdriver.Chrome(service=driver_service, options=chrome_options)
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

            for i, k in enumerate(yf_url):
                if not k.text:
                    continue
                if i == 1:
                    video_url = k.get_attribute('href')
                    video_title = k.text
                elif i == 2:
                    channel_url = k.get_attribute('href')
                    channel_name = k.text
                if i >= 2:
                    break
            unit = {'title': video_title, 'url': video_url, 'body': body, 'channel_name': channel_name,
                    'channel_url': channel_url}
            ans.append(unit)
        driver.close()
    except NoSuchElementException:
        print('\033[0mYT: {}'.format(url))
    return ans

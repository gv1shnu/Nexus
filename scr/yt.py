from scr.helpers import get_url
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.driver import driver_service
from selenium.common import NoSuchElementException, WebDriverException

chrome_options = Options()
chrome_options.add_argument("--headless --no-sandbox --disable-dev-shm-usage --disable-gpu")


def get_yt_results(query: str) -> list:
    """
    Scrapes search results from YouTube.

    Args:
        query (str): the search query.

    Returns: a list of dictionaries
    """
    engine_name = "YouTube"
    cards = list()
    url = get_url(q=query, base="https://www.youtube.com/", t="results?search_query")
    try:
        driver = webdriver.Chrome(service=driver_service, options=chrome_options)
        driver.get(url)
        elem = driver.find_element(By.ID, 'contents')
        children_elems = elem.find_elements(By.ID, 'dismissible')
        for child in children_elems:
            if child:
                yf = child.find_elements(By.CSS_SELECTOR, "yt-formatted-string")
                body = ""
                for i in yf:
                    if 'metadata' in i.get_attribute('class'):
                        body += i.text
                video_url, video_title, channel_url, channel_name = "", "", "", ""

                try:
                    text_wrapper_div = child.find_element(By.CSS_SELECTOR,
                                                          'div.text-wrapper.style-scope.ytd-video-renderer')
                    if text_wrapper_div:
                        div_meta = text_wrapper_div.find_element(By.ID, "meta")
                        if div_meta:
                            div_title_wrapper = div_meta.find_element(By.ID, "title-wrapper")
                            if div_title_wrapper:
                                h3_element = div_title_wrapper.find_element(By.TAG_NAME, 'h3')
                                if h3_element:
                                    anchor_tag = h3_element.find_element(By.CSS_SELECTOR, 'a#video-title')
                                    video_url = anchor_tag.get_attribute('href')
                                    video_title = anchor_tag.text

                    div_info = text_wrapper_div.find_element(By.ID, "channel-info")
                    if div_info:
                        div_container = div_info.find_element(By.ID, "container")
                        if div_container:
                            div_text_container = div_container.find_element(By.ID, "text-container")
                            if div_text_container:
                                anchor_tag = div_text_container.find_element(By.TAG_NAME, 'a')
                                channel_url = anchor_tag.get_attribute('href')
                                channel_name = anchor_tag.text
                except NoSuchElementException:
                    pass

                card = {'engine': engine_name, 'title': video_title, 'url': video_url, 'body': body,
                        'channel_name': channel_name,
                        'channel_url': channel_url}
                cards.append(card)
        driver.close()
    except (WebDriverException, NoSuchElementException) as e:
        print('\033[0m{}: {} - {}'.format(str(e), engine_name, url))
    return cards


# HTML tree structure
# ----- div#contents. style-scope ytd-item-section-renderer style-scope ytd-item-section-renderer
# ------ div#dismissible.style-scope ytd-video-renderer
#
# ------- div.text-wrapper style-scope ytd-video-renderer
# -------- div#meta.style-scope ytd-video-renderer
# --------- div#title-wrapper.style-scope ytd-video-renderer
# ---------- h3.title-and-badge style-scope ytd-video-renderer
# ----------- a#video-title.yt-simple-endpoint style-scope ytd-video-renderer (url, title)
#
# -------- div#channel-info.style-scope ytd-video-renderer
# --------- div.style-scope ytd-channel-name#container
# ---------- div.style-scope ytd-channel-name#text-container
# ---------- a (for channel name, url)
#
# -------- div.metadata-snippet-container style-scope ytd-video-renderer style-scope ytd-video-renderer
# --------- (span elements contain the description)



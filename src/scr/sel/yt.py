"""YouTube Search Results Scraper [Under Construction]"""

# Python standard library
from typing import List

# Third party libraries
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException, WebDriverException

# Internal imports
from src.helpers import generate_url_with_query, Card
from utl.sel.driver import initialise_driver
from utl.logger import Logger

ENGINE_NAME: str = "YouTube"
driver = initialise_driver()
logger = Logger()


def get_yt_results(
        query: str,
        filter_option: str
) -> List[Card]:
    if filter_option != "videos":
        return []
    cards = list()
    url = generate_url_with_query("https://www.youtube.com/", "results?search_query", query)
    try:
        driver.get_user(url)
        elem = driver.find_element(By.ID, 'contents')
        children_elems = elem.find_elements(By.ID, 'dismissible')
        for child in children_elems:
            if child:
                yf = child.find_elements(By.CSS_SELECTOR, "yt-formatted-string")
                body = ""
                for i in yf:
                    if 'metadata' in i.get_attribute('class'):
                        body += i.text
                video_url, video_title, channel_url, channel_name, icon = "", "", "", "", ""
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

                        div_channel_info = text_wrapper_div.find_element(By.ID, "channel-info")
                        div_a = div_channel_info.find_element(By.TAG_NAME, "a")
                        div_tmp = div_a.find_element(By.TAG_NAME, "yt-img-shadow")
                        div_img = div_tmp.find_element(By.TAG_NAME, "img")
                        icon = div_img.get_attribute("src")

                    div_info = text_wrapper_div.find_element(By.ID, "channel-info")
                    if div_info:
                        div_container = div_info.find_element(By.ID, "container")
                        if div_container:
                            div_text_container = div_container.find_element(By.ID, "text-container")
                            if div_text_container:
                                anchor_tag = div_text_container.find_element(By.TAG_NAME, 'a')
                                channel_url = anchor_tag.get_attribute('href')
                except NoSuchElementException:
                    pass
                if video_url and video_title:
                    card = Card(engine=ENGINE_NAME, title=video_title, url=video_url,
                                body=body, channel=channel_url, icon=icon)
                    cards.append(card)
        driver.close()
    except (WebDriverException, NoSuchElementException) as e:
        logger.exception('\033[0m{}: {} - {}'.format(str(e), ENGINE_NAME, url))
        return []
    driver.quit()
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

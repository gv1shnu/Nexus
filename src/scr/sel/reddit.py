"""Reddit Search Results Scraper [Under Construction]"""

# Python standard library
from typing import List

# Third party libraries
from selenium.common import WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By

# Internal imports
from utl.driver import initialise_driver
from utl.logger import Logger
from src.helpers import generate_url_with_query, Card

ENGINE_NAME = "Reddit"
driver = initialise_driver()
logger = Logger()


def get_reddit_results(
        query: str,
        filter_option: str
) -> List[Card]:
    if filter_option != "text":
        return []
    cards = list()
    url = generate_url_with_query('https://www.reddit.com/', 'search/?q=', query)
    try:
        driver.get(url)
        elem = driver.find_element(By.ID, "search-results-tab-slot")
        if elem:
            xl_divs = elem.find_elements(By.CLASS_NAME, "pb-xl")
            if xl_divs:
                for xl_div in xl_divs:
                    card = Card(engine=ENGINE_NAME)
                    full_div = xl_div.find_element(By.CLASS_NAME, "w-full")
                    if full_div:
                        t_div = full_div.find_element(By.CSS_SELECTOR, "div.text-neutral-content-weak.text-12.flex"
                                                                       ".items-center.mb-xs")
                        if t_div:
                            shr_div = t_div.find_element(By.TAG_NAME, "shreddit-async-loader")
                            if shr_div:
                                hov_div = shr_div.find_element(By.TAG_NAME, "faceplate-hovercard")
                                if hov_div:
                                    fp_div = hov_div.find_element(By.TAG_NAME, "faceplate-tracker")
                                    if fp_div:
                                        ar = fp_div.find_element(By.TAG_NAME, "a")
                                        if ar:
                                            card.channel_url, card.channel_name = ar.get_attribute(
                                                'href'), ar.text
                                            try:
                                                fimg = ar.find_element(By.TAG_NAME, "faceplate-img")
                                                if fimg:
                                                    card.icon = fimg.get_attribute('src')
                                            except:
                                                pass
                        fp2_div = full_div.find_elements(By.TAG_NAME, "faceplate-tracker")
                        if fp2_div:
                            f = fp2_div[-1]
                            afr = f.find_element(By.TAG_NAME, "a")
                            if afr:
                                title = afr.text
                                card.title, card.url = title, afr.get_attribute('href')
                    cards.append(card)
    except (WebDriverException, NoSuchElementException) as e:
        logger.error('\033[0m{}: {} - {}'.format(str(e), ENGINE_NAME, url))
        return []
    driver.quit()

    return cards


if __name__ == '__main__':
    x = get_reddit_results("asus vs hp", "text")
    for i in x:
        logger.info(f"{i}")


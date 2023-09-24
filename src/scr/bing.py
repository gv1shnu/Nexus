"""Bing Search Results Scraper"""
from typing import List
import bs4.element
from utils.helpers import is_valid_url, generate_url_with_query, get_container_from_parent, \
    find_all_containers_from_parent, get_soup, Card
from utils.logger import Logger

ENGINE_NAME = "Bing"
logger = Logger()


def get_card_from_li(
        li: bs4.element.Tag
) -> Card:
    card = Card(engine=ENGINE_NAME)
    cls = li.get_attribute('class')
    if "b_algo" in cls:
        div_tpcn = get_container_from_parent(li, 'div', ".tpcn")
        a = get_container_from_parent(div_tpcn, 'a', ".tilk")
        link = a['href']
        if is_valid_url(link):
            card.url = link
            # card["title"], card["icon"], card["channel_url"] = get_card_attributes(card["url"])
        else:
            logger.error("Invalid URL found")
        div_tptxt = get_container_from_parent(a, 'div', ".tptxt")
        div_tptt = get_container_from_parent(div_tptxt, 'div', ".tptt")
        card.channel_name = div_tptt.text
    return card


def get_bing_results(
        query: str,
        filter_option: str
) -> List[Card]:
    """
    Get search results from Bing search engine for a given query.

    Args:
        query (str): Query string.
        filter_option (str): filter string.

    Returns:
        list: List of dictionaries containing search result information.
    """
    if filter_option != "text":
        return []
    cards = list()
    url = generate_url_with_query(base_url="https://www.bing.com/", query_param="search?q", q=query)
    try:
        soup = get_soup(url)
        div_content = get_container_from_parent(soup, 'div', "#b_content")
        if div_content:
            div_results = get_container_from_parent(div_content, 'ol', "#b_results")
            if div_results:
                div_list = find_all_containers_from_parent(div_results, 'li')
                if div_list:
                    for li in div_list:
                        card = get_card_from_li(li)
                        logger.debug(card)
                        cards.append(card)
                        return [] #### Work in progress
                else:
                    logger.error("div_list invalid")
                    return []
            else:
                logger.error("div_results invalid")
                return []
        else:
            logger.error("div_content invalid")
            return []
    except Exception as e:
        logger.error('{}: {} - {}'.format(str(e), ENGINE_NAME, url))

    return cards


if __name__ == '__main__':
    bing_results = get_bing_results("web scraping", "text")
    # logger.debug(f"{len(bing_results)}")
    # for i in bing_results:
    #     print(i)

# HTML tree structure
# - div.b_content
# -- ol.b_results
# --- li.b_algo (card)
# ---- h2
# ----- a (url, title)
#
# ---- div.b_caption
# ----- p (body)

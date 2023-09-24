"""Bing Search Results Scraper [Under Construction]"""

# Python standard library
from typing import List

# Third party library
import bs4.element

# Internal imports
from src.helpers import generate_url_with_query, get_container_from_parent, \
    find_all_containers_from_parent, get_soup, Card, get_domain, get_icon
from utl.logger import Logger

ENGINE_NAME: str = "Bing"
logger = Logger()


def get_card_from_li(
        li: bs4.element.Tag
) -> Card | None:
    logger.debug(f"inside func")

    card = Card()
    cls = li.get('class')
    logger.debug(f"cls: {cls}")

    if cls:
        logger.debug(f"cls ok")

    if "b_algo" in cls:
        card.engine = ENGINE_NAME
        logger.debug(f"b_algo present")

        div_tpcn = get_container_from_parent(li, 'div', ".tpcn")
        if div_tpcn:
            logger.debug(f"div_tpcn ok")
            a = get_container_from_parent(div_tpcn, 'a', ".tilk")
            if a:
                logger.debug(f"a ok")
                link = a.get('href')
                logger.debug(f"link: {link}")
                if link:
                    (card.url, card.icon, card.channel_url) = (link,
                                                               get_icon(link),
                                                               get_domain(link))
                else:
                    logger.error("Empty URL found")
                div_tptxt = get_container_from_parent(a, 'div', ".tptxt")
                if div_tptxt:
                    logger.debug(f"div_tptxt ok")
                    div_tptt = get_container_from_parent(div_tptxt, 'div', ".tptt")
                    if div_tptt:
                        logger.debug(f"div-tptt ok")
                        card.channel_name = div_tptt.text
                    else:
                        logger.warning("div-tptt not ok")
                else:
                    logger.warning("div_tptxt not ok")
            else:
                logger.warning("a not ok")
                return None
        else:
            logger.warning("div_tpcn not ok")
            return None

        div_b_title = get_container_from_parent(li, 'div', '.b_title')
        if div_b_title:
            card.title = div_b_title.find('h2').find('a').text
            logger.info(f"{card.title}")
        else:
            logger.warning("div_b_title not ok")
            return None

        p_body = get_container_from_parent(li, 'p', ".b_lineclamp3")
        if p_body:
            card.body = p_body.text
    else:
        logger.debug("b_algo not in this item's class")
        return None

    return card

cnt = 0

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
    url: str = generate_url_with_query(base_url="https://www.bing.com/", query_param="search?q", q=query)
    # try:
    soup = get_soup(url)
    div_content = get_container_from_parent(soup, 'div', "#b_content")
    if div_content:
        logger.debug(f"div_content ok")
        div_results = get_container_from_parent(div_content, 'ol', "#b_results")
        if div_results:
            logger.debug(f"div_results ok")
            div_list = find_all_containers_from_parent(div_results, 'li')
            if div_list:
                logger.debug(f"div_list ok")
                for li in div_list:
                    if li:
                        logger.debug(f"li ok")
                        card = get_card_from_li(li)
                        if card:
                            logger.debug(f"card ok")
                            cards.append(card)

                            if cnt > 2:
                                break

                        else:
                            logger.warning("empty card")
                    else:
                        logger.warning("li not ok")
            else:
                logger.warning("div_list invalid")
                return []
        else:
            logger.warning("div_results invalid")
            return []
    else:
        logger.warning("div_content invalid")
        return []
    # except Exception as e:
    #     logger.error('{}: {} - {}'.format(str(e), ENGINE_NAME, url))

    return cards


if __name__ == '__main__':
    bing_results = get_bing_results("web scraping v data mining", "text")
    logger.debug(f"results count: {len(bing_results)}")
    for i in bing_results:
        logger.info(f"{i}")
        print()

# HTML tree structure
# - div.b_content
# -- ol.b_results
# --- li.b_algo (card)
# ---- h2
# ----- a (url, title)
#
# ---- div.b_caption
# ----- p (body)

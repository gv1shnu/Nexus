"""Google search results scraper"""

# Python standard libraries
from typing import List

# Third party libraries
import requests

# Internal imports
from src.helpers import get_domain, Card, get_soup, generate_url_with_query
from utl.logger import Logger
from decl import MAX_LIMIT_PER_ENGINE

ENGINE_NAME: str = "Google"
logger = Logger()


def search(url: str) -> tuple:
    soup = get_soup(url)
    result_block = soup.find_all("div", attrs={"class": "g"})
    for result in result_block:
        link = result.find("a", href=True)
        title = result.find("h3")
        description_box = result.find(
            "div", {"style": "-webkit-line-clamp:2"})
        if description_box:
            description = description_box.text
            if link and title and description:
                yield link["href"], title.text, description


def get_google_results(
        query: str,
        filter_option: str
) -> List[Card]:
    """
    :param query:  Query string.
    :param filter_option: filter string
    :return: List of cards containing search result information.
    """
    if filter_option != "text":
        return []
    cards = list()
    try:
        dips: tuple = search(
            generate_url_with_query(
                "https://www.google.com/",
                "search?q",
                query,
                MAX_LIMIT_PER_ENGINE
            )
        )
        for dip in dips:
            url: str = dip[0]
            channel_url: str = "https://" + get_domain(url)
            card = Card(
                engine=ENGINE_NAME, title=dip[1],
                url=url, channel=channel_url,
                body=dip[2]
            )
            cards.append(card)
    except requests.exceptions.HTTPError:
        logger.error("{}-Too Many Requests\n".format(ENGINE_NAME))
        return []
    except Exception as e:
        logger.error(f"An error occurred while fetching google results: {e}")
        return []
    return cards

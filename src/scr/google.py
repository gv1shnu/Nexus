# Python standard library
import time
from typing import List

# Third party libraries
import requests
from googlesearch import search

# Internal imports
from src.helpers import get_domain, Card, get_icon
from utl.logger import Logger

ENGINE_NAME = "Google"
logger = Logger()


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
        dips = search(query, advanced=True)
        for dip in dips:
            url = dip.url
            icon = get_icon(url)
            time.sleep(0.5)
            channel_url = "https://" + get_domain(url)
            channel_name = channel_url.split('.')[1]
            card = Card(
                engine=ENGINE_NAME, title=dip.title,
                url=url, channel_name=channel_name,
                channel_url=channel_url,
                body=dip.description, icon=icon
            )
            cards.append(card)
    except requests.exceptions.HTTPError:
        logger.error("{}-Too Many Requests\n".format(ENGINE_NAME))
        return []
    except Exception as e:
        logger.error(f"An error occurred while fetching google results: {e}")
        return []
    return cards

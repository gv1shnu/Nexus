import time
from typing import List
import favicon
from googlesearch import search
from utils.helpers import get_domain, Card
import requests
from utils.logger import Logger

ENGINE_NAME = "Google"
logger = Logger()


def get_google_results(
        query: str,
        filter_option: str
) -> List[Card]:
    """
    :param query:  Query string.
    :param filter_option:
    :return: List of dictionaries containing search result information.
    """
    if filter_option != "text":
        return []
    cards = []
    try:
        dips = search(query, advanced=True)
        for dip in dips:
            url = dip.url
            icon = favicon.get(url)[0].url
            time.sleep(0.5)
            channel_url = "https://"+get_domain(url)
            channel_name = channel_url.split('.')[1]
            card = Card(engine=ENGINE_NAME, title=dip.title, url=url, channel_name=channel_name, channel_url=channel_url,
                        body=dip.description, icon=icon)
            cards.append(card)
    except requests.exceptions.HTTPError:
        logger.error("{}-Too Many Requests\n".format(ENGINE_NAME))
        return []
    except Exception as e:
        logger.error(f"An error occurred while fetching google results: {e}")
        return []
    return cards

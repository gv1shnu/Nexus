from googlesearch import search
from src.helpers import get_domain
import requests


def get_google_results(query: str) -> list:
    """
    Scrapes search results from Google.

    Args:
        query (str): The search query

    Returns: list of dictionaries
    """
    cards = []
    engine_name = "Google"
    try:
        dips = search(query, advanced=True)
        cards += [{
            'engine': engine_name,
            'title': dip.title,
            'url': dip.url,
            'channel_name': get_domain(dip.url),
            'channel_url': get_domain(dip.url),
            'body': dip.description
        } for dip in dips]
    except requests.exceptions.HTTPError:
        print("{}-Too Many Requests\n".format(engine_name))
    return cards

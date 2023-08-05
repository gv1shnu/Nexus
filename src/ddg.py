from duckduckgo_search import DDGS
from src.helpers import get_domain


def get_ddg_results(query: str) -> list:
    """
    Scrapes search results from Duckduckgo.

    Args:
        query (str): the search query

    Returns: a list of dictionaries
    """
    engine_name = "Duckduckgo"
    cards = [{
        'engine': engine_name,
        'title': r['title'],
        'url': r['href'],
        'channel_name': get_domain(r['href']),
        'channel_url': get_domain(r['href']),
        'body': r['body']
    } for r in DDGS().text(query)]
    return cards

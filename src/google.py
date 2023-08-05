from googlesearch import search
from src.helpers import get_domain
import requests


def get_res(query: str) -> list:
    """
    Scrapes search results from Google.

    Args:
        query (str): The search query

    Returns: list of dictionaries
    """
    ans = []
    try:
        dips = search(query, advanced=True)
        ans += [{
            'title': dip.title,
            'url': dip.url,
            'channel_name': get_domain(dip.url),
            'channel_url': get_domain(dip.url),
            'body': dip.description
        } for dip in dips]
    except requests.exceptions.HTTPError:
        print("Too Many Requests\n")
    return ans

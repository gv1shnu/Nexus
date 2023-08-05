from duckduckgo_search import DDGS
from scr.helpers import get_domain


def get_ddg_results(query: str) -> list:
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

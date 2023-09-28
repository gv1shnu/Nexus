"""Duckduckgo search results scraper"""

# Python standard libraries
from typing import List
import httpx

# Third party libraries
from requests.exceptions import HTTPError
from duckduckgo_search import DDGS

# Internal imports
from src.helpers import get_domain, Card, get_header
from utl.logger import Logger
from decl import MAX_LIMIT_PER_ENGINE

ENGINE_NAME: str = "Duckduckgo"
logger = Logger()


def get_ddg_results(
        query: str,
        filter_option: str
) -> List[Card]:
    cards = list()
    try:
        cnt: int = 0
        if filter_option == "text":
            for r in DDGS(headers=get_header()).text(query):
                url: str = r["href"]
                channel_url: str = "https://" + get_domain(url)
                card = Card(
                    title=r['title'], url=r['href'],
                    channel=channel_url, body=r['body'],
                    engine=ENGINE_NAME
                )
                cnt += 1
                if cnt > MAX_LIMIT_PER_ENGINE:
                    break
                cards.append(card)
        elif filter_option == "images":
            for r in DDGS(headers=get_header()).images(query):
                card = Card(
                    title=r['title'], url=r['image'],
                    channel=r['source'], body=r['image'],
                    icon=r['thumbnail'],
                    engine=ENGINE_NAME
                )
                cnt += 1
                if cnt > MAX_LIMIT_PER_ENGINE:
                    break
                cards.append(card)
        elif filter_option == "videos":
            for r in DDGS(headers=get_header()).videos(query):
                card = Card(
                    title=r['title'], url=r['content'],
                    channel=f"https://www.youtube.com/@{r['uploader'].replace(' ', '')}"
                    if r['publisher'] == 'YouTube' else None, body=r['description'],
                    icon=r['images']['small'],
                    engine=ENGINE_NAME
                )
                cnt += 1
                if cnt > MAX_LIMIT_PER_ENGINE:
                    break
                cards.append(card)
        elif filter_option == "news":
            for r in DDGS(headers=get_header()).news(query):
                card = Card(
                    title=r['title'], url=r['href'],
                    channel=r['source'], body=r['body'],
                    icon=r['image'],
                    engine=ENGINE_NAME
                )
                cnt += 1
                if cnt > MAX_LIMIT_PER_ENGINE:
                    break
                cards.append(card)
        else:
            logger.error("Invalid filter option")
            return []
    except (HTTPError, httpx.HTTPStatusError, Exception) as e:
        logger.exception(f"An error occurred while fetching DDG results: {e}")
        return []
    return cards

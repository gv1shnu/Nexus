"""Duckduckgo search results scraper"""

# Python standard libraries
from typing import List
import httpx

# Third party libraries
from requests.exceptions import HTTPError
from duckduckgo_search import DDGS

# Internal imports
from src.helpers import get_domain, Card, get_header, relevance_score_calculator
from utl.logger import Logger

ENGINE_NAME: str = "Duckduckgo"
logger = Logger()


def get_ddg_results(
        query: str,
        filter_option: str
) -> List[Card]:
    cards = list()
    try:
        if filter_option == "text":
            for r in DDGS(headers=get_header()).text(query):
                url: str = r["href"]
                channel_url: str = "https://" + get_domain(url)
                card = Card(
                    title=r['title'], url=r['href'],
                    channel=channel_url, body=r['body'],
                    engine=ENGINE_NAME, relevance=relevance_score_calculator(
                        document=r['title']+r['body'], input_keyword=query
                    ), icon=None
                )
                cards.append(card)
        elif filter_option == "images":
            for r in DDGS(headers=get_header()).images(query):
                card = Card(
                    title=r['title'], url=r['image'],
                    channel=r['source'], body=r['image'],
                    icon=r['thumbnail'],
                    engine=ENGINE_NAME, relevance=relevance_score_calculator(
                        document=r['image'], input_keyword=query
                    )
                )
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
                cards.append(card)
        elif filter_option == "news":
            for r in DDGS(headers=get_header()).news(query):
                card = Card(
                    title=r['title'], url=r['href'],
                    channel=r['source'], body=r['body'],
                    icon=r['image'],
                    engine=ENGINE_NAME, relevance=relevance_score_calculator(
                        document=r['body'], input_keyword=query
                    )
                )
                cards.append(card)
        else:
            logger.error("Invalid filter option")
            return []
    except (HTTPError, httpx.HTTPStatusError, Exception) as e:
        logger.exception(f"An error occurred while fetching DDG results: {e}")
        return []
    return cards

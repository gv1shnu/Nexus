from typing import List
import httpx
from duckduckgo_search import DDGS
from utils.helpers import get_domain, Card
import favicon
from utils.logger import Logger

ENGINE_NAME = "Duckduckgo"
logger = Logger()


def get_ddg_results(
        query: str,
        filter_option: str
) -> List[Card]:
    try:
        cards = []
        if filter_option == "text":
            for r in DDGS().text(query):
                url = r["href"]
                icon = favicon.get(url)[0].url
                channel_url = "https://" + get_domain(url)
                channel_name = channel_url.split('.')[1]
                card = Card(title=r['title'], url=r['href'],
                            channel_name=channel_name,
                            channel_url=channel_url, body=r['body'],
                            icon=icon,
                            engine=ENGINE_NAME)
                cards.append(card)
        elif filter_option == "images":
            for r in DDGS().images(query):
                card = Card(title=r['title'], url=r['image'],
                            channel_name=r['source'],
                            channel_url=None, body=r['image'],
                            icon=r['thumbnail'],
                            engine=ENGINE_NAME)
                cards.append(card)
        elif filter_option == "videos":
            for r in DDGS().videos(query):
                card = Card(title=r['title'], url=r['content'],
                            channel_name=r['uploader'],
                            channel_url=f"https://www.youtube.com/@{r['uploader'].replace(' ', '')}"
                            if r['publisher'] == 'YouTube' else None, body=r['description'],
                            icon=r['images']['small'],
                            engine=ENGINE_NAME)
                cards.append(card)
        elif filter_option == "news":
            for r in DDGS().news(query):
                card = Card(title=r['title'], url=r['href'],
                            channel_name=r['source'],
                            channel_url=None, body=r['body'],
                            icon=r['image'],
                            engine=ENGINE_NAME)
                cards.append(card)
        else:
            logger.error("Invalid filter option")
            return []
        return cards
    except (httpx.HTTPStatusError, Exception) as e:
        logger.exception(f"An error occurred while fetching DDG results: {e}")
        return []

"""Yahoo Search Results Scraper [In-Progress]"""

# Python standard libraries
import time
from typing import List

# Internal imports
from src.helpers import generate_url_with_query, get_domain, get_soup, Card, relevance_score_calculator
from utl.logger import Logger

ENGINE_NAME = "Yahoo"
logger = Logger()


def get_yahoo_results(
        query: str,
        filter_option: str
) -> List[Card]:
    if filter_option != "text":
        return []
    url = generate_url_with_query('https://search.yahoo.com/', 'search?q', query)
    cards = list()
    start_time = time.time()
    try:
        soup = get_soup(url)
        if soup:
            ol = soup.find('ol', class_=lambda lmb: lmb and 'searchCenterMiddle' in lmb)
            if ol:
                lis = ol.find_all('li')
                for li in lis:
                    if li:
                        card = Card(engine=ENGINE_NAME)
                        div1 = li.find('div', class_=lambda lmb: lmb and 'algo' in lmb)
                        if div1:
                            div_title_url = div1.find('div', class_="compTitle options-toggle")
                            if div_title_url:
                                h3 = div_title_url.find('h3')
                                if h3:
                                    anchor_tag = h3.find('a')
                                    if anchor_tag:
                                        aria = anchor_tag.get('aria-label')
                                        if aria:
                                            card.title = aria
                                        href = anchor_tag.get('href')
                                        if href:
                                            card.url = href
                            div_body = li.find('div', class_="compText aAbs")
                            if div_body:
                                p_element = div_body.find('p')
                                if p_element:
                                    span = p_element.find('span', class_="fc-falcon")
                                    if span:
                                        card.body = span.text
                            if card.title and card.url:
                                card.channel = "https://"+get_domain(card.title)
                                card.rel = relevance_score_calculator(
                                    document=card.title+card.body, input_keyword=query
                                )
                                cards.append(card)
                    if time.time() - start_time > 5:
                        logger.info("Time limit crossed. Returning")
                        return cards
    except Exception as e:
        logger.error('\033[0m{}: {} - {}'.format(str(e), ENGINE_NAME, url))
    return cards


# HTML tree structure
# ------- ol.reg  searchCenterMiddle
# -------- li
# --------- div.(class must contain 'algo')
# ---------- div.compTitle options-toggle
# ----------- h3
# ------------ a (for title, url)
#
# ---------- div.compText aAbs
# ----------- p
# ------------ span. fc-falcon (for body)

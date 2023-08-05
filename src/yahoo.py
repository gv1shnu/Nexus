import requests
from src.helpers import get_url, is_valid_url, get_header, get_domain
from bs4 import BeautifulSoup


def get_yahoo_results(query: str) -> list:
    """
    Scrapes search results from Yahoo.

    Args:
        query (str): the search query

    Returns: a list of dictionaries
    """
    engine_name = "Yahoo"
    base_url = get_url(q=query, base='https://search.yahoo.com/', t='search?q')
    header = get_header()
    response = requests.get(base_url, headers=header)
    cards = list()
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
        result_container = soup.find('ol', class_='reg searchCenterMiddle')
        if result_container:
            for li in result_container.find_all('li'):
                unit = {'title': None, 'url': None, 'body': None}
                div = li.find('div', class_="compTitle options-toggle")
                if div:
                    h3 = div.find('h3')
                    if h3:
                        anchor_tag = h3.find('a')
                        if anchor_tag:
                            unit['title'] = anchor_tag.get_text(strip=True)
                            if is_valid_url(anchor_tag['href']):
                                unit['url'] = anchor_tag['href']
                p_div = li.find('div', class_="compText aAbs")
                if p_div:
                    p_element = p_div.find('p')
                    if p_element:
                        unit['body'] = p_element.find('span').text

                if unit['title'] and unit['url']:
                    unit['channel_name'] = get_domain(unit['title'])
                    unit['channel_url'] = get_domain(unit['title'])
                    unit['engine'] = engine_name
                    cards.append(unit)
    except Exception:
        print('\033[0m{}. {}'.format(engine_name, response.url))
    return cards

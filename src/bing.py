import requests
from bs4 import BeautifulSoup
from src.helpers import is_valid_url, get_domain, get_url, get_header


def get_bing_results(query: str) -> list:
    """
    Scrapes search results from Bing.

    Args:
        query (str): the search query

    Returns: list of dictionaries
    """
    cards = list()
    url = get_url(q=query, base="https://www.bing.com/", t="search?q")
    engine_name = "Bing"
    try:
        header = get_header()
        response = requests.get(url, headers=header).content
        soup = BeautifulSoup(response, 'html.parser')
        data1 = soup.find('ol', id='b_results')
        if data1:
            data2 = data1.find_all("li")
            for li in data2:
                unit = {'title': None, 'url': None, 'body': None}
                h2_element = li.find('h2')
                caption = li.find('div', class_="b_caption")
                if h2_element:
                    anchor_tag = h2_element.find('a')
                    if anchor_tag:
                        if is_valid_url(anchor_tag['href']):
                            unit['title'], unit['url'] = h2_element.text, anchor_tag['href']
                if caption:
                    p_tag = caption.find('p')
                    if p_tag:
                        unit['body'] = p_tag.text[3:]

                if unit['title'] and unit['url']:
                    unit['channel_name'] = get_domain(unit['url'])
                    unit['channel_url'] = get_domain(unit['url'])
                    unit['engine'] = engine_name
                    cards.append(unit)
    except Exception:
        print('\033[0m{}. {}'.format(engine_name, url))
    return cards

from scr.helpers import get_url, is_valid_url, get_domain, getSoup


def get_yahoo_results(query: str) -> list:
    """
    Scrapes search results from Yahoo.

    Args:
        query (str): the search query

    Returns: a list of dictionaries
    """
    engine_name = "Yahoo"
    url = get_url(q=query, base='https://search.yahoo.com/', t='search?q')
    cards = list()
    try:
        soup = getSoup(url)
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
    except Exception as e:
        print('\033[0m{}: {} - {}'.format(str(e), engine_name, url))
    return cards

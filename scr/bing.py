from scr.helpers import is_valid_url, get_domain, get_url, getSoup


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
        soup = getSoup(url)
        data1 = soup.find('ol', id='b_results')
        if data1:
            data2 = data1.find_all("li")
            for li in data2:
                card = {'title': None, 'url': None, 'body': None}
                h2_element = li.find('h2')
                caption = li.find('div', class_="b_caption")
                if h2_element:
                    anchor_tag = h2_element.find('a')
                    if anchor_tag:
                        if is_valid_url(anchor_tag['href']):
                            card['title'], card['url'] = h2_element.text, anchor_tag['href']
                if caption:
                    p_tag = caption.find('p')
                    if p_tag:
                        card['body'] = p_tag.text[3:]

                if card['title'] and card['url']:
                    card['channel_name'] = get_domain(card['url'])
                    card['channel_url'] = get_domain(card['url'])
                    card['engine'] = engine_name
                    cards.append(card)
    except Exception as e:
        print('\033[0m{}: {} - {}'.format(str(e), engine_name, url))
    return cards

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
        if soup:
            data1 = soup.find('div', id="b_content")
            if data1:
                ol = data1.find('ol', id='b_results')
                if ol:
                    data2 = ol.find_all("li", class_=lambda lmb: lmb and 'b_algo' in lmb)
                    if data2:
                        for li in data2:
                            card = {'title': None, 'url': None, 'body': None}
                            h2_element = li.find('h2')
                            if h2_element:
                                anchor_tag = h2_element.find('a')
                                if anchor_tag:
                                    if is_valid_url(anchor_tag['href']):
                                        card['title'], card['url'] = anchor_tag.text, anchor_tag['href']
                            div_caption = li.find('div', class_=lambda lmb: lmb and 'b_caption' in lmb)
                            if div_caption:
                                p_tag = div_caption.find('p')
                                if p_tag:
                                    card['body'] = p_tag.text

                            if card['title'] and card['url']:
                                card['channel_name'] = get_domain(card['url'])
                                card['channel_url'] = get_domain(card['url'])
                                card['engine'] = engine_name
                                cards.append(card)
    except Exception as e:
        print('\033[0m{}: {} - {}'.format(str(e), engine_name, url))
    return cards


# HTML tree structure
# - div.b_content
# -- ol.b_results
# --- li.b_algo (card)
# ---- h2
# ----- a (url, title)
#
# ---- div.b_caption
# ----- p (body)

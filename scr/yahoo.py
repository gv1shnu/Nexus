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
        if soup:
            ol = soup.find('ol', class_=lambda lmb: lmb and 'searchCenterMiddle' in lmb)
            if ol:
                lis = ol.find_all('li')
                for li in lis:
                    if li:
                        card = {'title': None, 'url': None, 'body': None}
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
                                            card['title'] = aria
                                        href = anchor_tag.get('href')
                                        if is_valid_url(href):
                                            card['url'] = href
                            div_body = li.find('div', class_="compText aAbs")
                            if div_body:
                                p_element = div_body.find('p')
                                if p_element:
                                    span = p_element.find('span', class_="fc-falcon")
                                    if span:
                                        card['body'] = span.text

                            if card['title'] and card['url']:
                                card['channel_name'] = get_domain(card['title'])
                                card['channel_url'] = get_domain(card['title'])
                                card['engine'] = engine_name
                                cards.append(card)
    except Exception as e:
        print('\033[0m{}: {} - {}'.format(str(e), engine_name, url))
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

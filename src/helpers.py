"""Helper functions for web scrapers"""

# Python standard libraries
from random import shuffle
from typing import List

# Third party libraries
import bs4.element
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import favicon
from requests.exceptions import HTTPError

# Internal imports
from utl.logger import Logger
from decl import Card, Pages, Page

logger = Logger()


def get_icon(url: str) -> str | None:
    try:
        return favicon.get(
            url,
            headers=get_header(),
            allow_redirects=False
        )[0].url
    except (IndexError, HTTPError):
        return None


def get_domain(url: str) -> str:
    """
    Get the domain from a URL.

    :param url: URL to extract the domain from.
    :return: Extracted domain.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc


# in-PROGRESS
def get_container_from_parent(parent_div: bs4.element.Tag, container_to_get: str,
                              selector=None) -> bs4.element.Tag or None:
    """
    Finds and returns a container element within a parent div using a CSS selector.

    :param parent_div: The parent div element where the search should be conducted.
    :param container_to_get: The tag name of the container element to look for (e.g., 'div', 'section').
    :param selector: The CSS selector to identify the specific container element.

    :return: The container element if found, or None if not found.
    """
    try:
        if selector:
            if isinstance(selector, list):
                selector = "".join(map(lambda word: "." + word, selector))
            container = parent_div.select_one(container_to_get + selector)
        else:
            container = parent_div.find(container_to_get, recursive=False)
        if container and container.name == container_to_get:
            return container
        return None
    except Exception as e:
        logger.error(f"Error finding {container_to_get}{selector} in {parent_div}: {e}")
        return None


# in-PROGRESS
def find_all_containers_from_parent(parent_div: bs4.element.Tag, container_to_get: str, selector=None) -> list:
    """
    Finds and returns all container elements within a parent div using a CSS selector.

    :param parent_div: The parent div element where the search should be conducted.
    :param container_to_get: The tag name of the container elements to look for (e.g., 'div', 'section').
    :param selector: The CSS selector to identify the specific container elements.

    :return: A list of bs4.element.Tag objects representing the matching container elements.
    """
    try:
        if selector:
            containers = parent_div.select(selector)
        else:
            containers = parent_div.find_all(container_to_get, recursive=False)
        matching_containers = [container for container in containers if container.name == container_to_get]
        return matching_containers
    except Exception as e:
        logger.error(f"Error finding {container_to_get}{selector} in {parent_div}: {e}")
        return []


def get_soup(url: str) -> BeautifulSoup or None:
    """
    Get a BeautifulSoup object from a URL.

    :param url: URL to fetch and parse.
    :return: Parsed BeautifulSoup object or None if the request fails.
    """
    header = get_header()
    try:
        response = requests.get(url, headers=header)
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while fetching {url}: {e}")
        return None


def generate_url_with_query(base_url: str, query_param: str, q: str, num: int | None = None) -> str:
    """
    Generate a URL with query parameters.

    :param base_url: Base URL.
    :param query_param: Query parameter identifier.
    :param q: Query.
    :param num: limiting result number.
    :return: Constructed URL with query parameters.
    """
    query_string = "+".join(q.split(' '))
    constructed_url = f"{base_url}{query_param}={query_string}"
    if num:
        constructed_url += f'&num={num}'
    logger.debug(f"Constructed URL: {constructed_url}")
    return constructed_url


def get_header() -> dict:
    """
    Get a random User-Agent header.

    :return: HTTP headers.
    """
    ua = UserAgent()
    return {'User-Agent': ua.random}


def get_current_page(
        page_number: int,
        data_list: Pages
) -> Page:
    """
    Retrieve the data corresponding to the specified page number from a data list.

    :param page_number: The page number to retrieve data for (1-indexed).
    :param data_list: A list containing data to be paginated.
    :return: A list containing data from the specified page, or an empty list if the page number is out of range.
    """
    _index = page_number - 1
    if 0 <= _index < len(data_list):
        return data_list[_index]
    return []


def remove_duplicate_cards(my_list: List[Card]) -> List[Card]:
    """
    Remove duplicates from a list of cards based on the 'url' attribute.

    :param my_list: A list of Card objects.
    :return: A new list containing only unique Card objects based on the 'url' attribute.
    """
    unique_urls = set()
    unique_items = list()
    for item in my_list:
        if item.url not in unique_urls:
            unique_urls.add(item.url)
            unique_items.append(item)
    shuffle(unique_items)
    return unique_items


def pagify(
        my_list: List[Card],
        items_per_page: int
) -> Pages:
    """
    Split a list into multiple pages, each containing a specified number of items.

    :param my_list: The list to be paginated.
    :param items_per_page: The maximum number of items per page.
    :return: A list of lists, where each inner list represents a page with up to 'items_per_page' items.
    """
    total_pages: int = len(my_list) // items_per_page + 1
    pages = list()
    for page in range(total_pages):
        start_index: int = page * items_per_page
        end_index: int = start_index + items_per_page
        items: Page = my_list[start_index:end_index]
        pages.append(items)
    return pages

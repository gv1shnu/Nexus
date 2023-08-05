# helper functions for scrapers

from urllib.parse import urlparse
import random


def get_domain(url: str) -> str:
    """
    Extracts the domain from a URL.

    Args:
        url (str): The URL to extract the domain from.

    Returns:
        str: The domain extracted from the URL.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc


def is_valid_url(url: str) -> bool:
    """
    Checks if a URL is valid.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def get_url(q: str, base: str, t: str) -> str:
    """
    Generates a URL for a given query, base URL, and query parameter.

    Args:
        q (str): The query string.
        base (str): The base URL.
        t (str): The query parameter.

    Returns:
        str: The generated URL.
    """
    x = "+".join(q.split(' '))
    return f"{base}{t}={x}"


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.48 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.55 Safari/537.36'
]


def get_header() -> dict:
    """
    Generates a random User-Agent header.

    Returns:
        dict: The generated User-Agent header.
    """
    tmp = random.choice(user_agents)
    return {'User-Agent': tmp}

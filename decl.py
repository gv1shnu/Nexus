# Python standard library
from typing import List

MODE: str = "DEBUG"  # "PRODUCTION"


class Card:
    def __init__(
            self, title=None, url=None,
            body=None, channel=None,
            icon=None, engine=None
    ):
        self.title = title
        self.url = url
        self.body = body
        self.channel = channel
        self.icon = icon
        self.engine = engine

    def __str__(self):
        return f'<Card data: {self.title}>'

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)


Page = List[Card]

Pages = List[Page]

MAX_LIMIT_PER_ENGINE: int = 42

ITEMS_PER_PAGE: int = 6

# Predefined options and filters for the search
OPTIONS: list = [
    "Google", "Bing", "Duckduckgo",
    "Yahoo", "YouTube", "Reddit"
]

FILTERS: list = [
    "Text", "Images",
    "Videos", "News"
]

# Path for chromedriver to be stored
CDR_PATH: str = "./cdr"

# Since, host is Linux-based. Only that exec and driver is required.
SUPPORTED_PLATFORM: str = "Linux"

# URL to download latest chromedriver from
CFT_URL: str = "https://googlechromelabs.github.io/chrome-for-testing/"


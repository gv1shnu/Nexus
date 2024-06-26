# Python standard libraries
import platform
import os
from typing import List

MODE: str = "DEBUG"  #PRODUCTION

INDEX_TEMPLATE: str = "index.html"
ERROR_TEMPLATE: str = "error.html"
RESULT_TEMPLATE: str = "results.html"


class Card:
    def __init__(
            self, title=None, url=None,
            body=None, channel=None,
            icon=None, engine=None, relevance=None
    ):
        self.title = title
        self.url = url
        self.body = body
        self.channel = channel
        self.icon = icon
        self.engine = engine
        self.rel = relevance

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'body': self.body,
            'channel': self.channel,
            'icon': self.icon,
            'engine': self.engine,
            'rel': self.rel
        }

    def __str__(self):
        return f'<Card data: {self.title}>'

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)


Page = List[Card]

Pages = List[Page]

ITEMS_PER_PAGE: int = 7

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

SUPPORTED_PLATFORMS: List[str] = ["Linux", "Windows"]

OS_NAME: str = platform.system()

PLATFORM_NAME: str = "linux64" if OS_NAME == "Linux" else "win64"

CHROMEDRIVER_PATH: str = (
        f"{CDR_PATH}/" +
        (
            "chromedriver"
            if OS_NAME == "Linux"
            else "chromedriver.exe"
        )
)

ROUTES: List[str] = [
    "/",
    "/submit",
    "/result"
]

# URL to download latest chromedriver from
CFT_URL: str = "https://googlechromelabs.github.io/chrome-for-testing/"

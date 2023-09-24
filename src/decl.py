# Python standard library
from typing import List


class Card:
    def __init__(
            self, title=None, url=None, body=None,
            channel_url=None, channel_name=None,
            icon=None, engine=None
    ):
        self.title = title
        self.url = url
        self.body = body
        self.channel_url = channel_url
        self.channel_name = channel_name
        self.icon = icon
        self.engine = engine

    def __str__(self):
        return f'<Card data: {self.title}>'


Page = List[Card]

Pages = List[Page]

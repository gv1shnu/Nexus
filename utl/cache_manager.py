# Standard libraries
import json
from pathlib import Path

# Third party libraries
from flask_caching import Cache

from src.helpers import Card


class PagesEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


class CacheManager:
    """
    Manages caching operations using Flask-Caching.

    Args:
        app: The Flask application instance.
    """

    def __init__(self, app):
        self.cache = Cache(
            app=app, config={
                "CACHE_TYPE": "filesystem",
                'CACHE_DIR': Path('./tmp')
            }
        )

    def cachify(self, variable, variable_handle: str):
        """
        Serialize and cache a variable.

        :param variable: The variable to be cached.
        :param variable_handle: Identifier for the cached variable.
        """
        serialized_pages = json.dumps(variable, cls=PagesEncoder)
        self.cache.set(variable_handle, serialized_pages)

    def get_from_cache(self, variable_handle: str):
        """
        Retrieve a deserialized variable from the cache.

        :param variable_handle: Identifier of the cached variable.
        :return: Any: The deserialized variable or None if not found.
        """
        deserialized_pages = self.cache.get(variable_handle)
        return json.loads(deserialized_pages)

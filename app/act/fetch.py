# Python standard library
import time
from typing import List, Dict

# Third-party libraries
from flask import (
    Blueprint, request,
    redirect, url_for,
    session, current_app
)

# Internal imports
from src.scrape import Scrape
from utl.logger import Logger
from decl import Pages
from src.handler import Handler

fetch_bp = Blueprint('fetch', __name__)
logger = Logger()


# submit route of the fetch blueprint
@fetch_bp.route(
    '/submit', methods=['POST']
)
def submit():
    # Fetch the POST requests from index route
    if request.method == 'POST':
        query: str = request.form.get('q')
        selected_options: list = request.form.getlist('options')
        filter_option: str = request.form.get('filter')
    else:
        logger.error("Invalid request method")
        return

    try:
        handler = Handler()
        start: float = time.perf_counter()
        data: List[Dict] = handler.get_search_history(query, selected_options, filter_option)
        if data:
            pages: Pages = data[0]['results']
            count: int = data[0]['count']
        else:
            scraper = Scrape()
            pages: Pages = scraper.get_results(
                (query, selected_options, filter_option)
            )
            count: int = sum([
                len(i) for i in pages
            ])
        end: float = time.perf_counter()
        duration = round(end - start, 1)

        cache_manager = current_app.extensions.get('cache_manager')
        cache_manager.cachify(pages, "pages")

        (
            session["query"],
            session["count"],
            session["duration"]
        ) = (
            query,
            count,
            duration
        )

    except Exception as e:
        logger.error(f"Error in handler: {e}")
        return

    # redirect to results page
    return redirect(url_for("res.index"))

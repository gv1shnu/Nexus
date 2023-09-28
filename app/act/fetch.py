# Python standard library
import time

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

fetch_bp = Blueprint('fetch', __name__)
logger = Logger()


# submit route of the fetch blueprint
@fetch_bp.route(
    '/submit', methods=['POST']
)
def submit():
    # Fetch the POST requests from index route
    query: str = request.form.get('q')
    selected_options: list = request.form.getlist('options')
    filter_option: str = request.form.get('filter')

    start: float = time.perf_counter()
    scraper = Scrape()
    pages: Pages = scraper.get_results(
        (query, selected_options, filter_option)
    )
    end: float = time.perf_counter()
    duration = round((end - start), 2)

    cache_manager = current_app.extensions['cache_manager']
    cache_manager.cachify(pages, "pages")

    (
        session["query"],
        session["count"],
        session["duration"]
    ) = (
        query,
        len(pages) * 7,
        duration
    )

    # redirect to results page
    return redirect(url_for("res.index"))

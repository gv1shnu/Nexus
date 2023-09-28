# Third-party libraries
from flask import Blueprint, abort, render_template, session, request, current_app
from jinja2 import TemplateNotFound

# Python standard libraries
from concurrent.futures import ThreadPoolExecutor
import time

# Internal imports
from src.helpers import get_current_page, get_icon
from utl.logger import Logger
from decl import Pages, Page, Card, ITEMS_PER_PAGE

res_bp = Blueprint('res', __name__)
logger = Logger()


def update_icon_for_card(card: Card):
    card["icon"] = get_icon(card["url"])


# index route of the res blueprint
@res_bp.route(
    '/result'
)
def index():
    try:
        cache_manager = current_app.extensions['cache_manager']
        pages: Pages = cache_manager.get_from_cache("pages")

        page_number = int(request.args.get('page', 1))
        current_page: Page = get_current_page(
            page_number, pages
        )

        # Update icon links here, to reduce n/w overload
        start: float = time.perf_counter()
        with ThreadPoolExecutor(max_workers=ITEMS_PER_PAGE) as executor:
            futures = list()
            for card in current_page:
                future = executor.submit(
                    update_icon_for_card,
                    card
                )
                futures.append(future)
            for future in futures:
                future.result()
        end: float = time.perf_counter()
        logger.info(f"Fetching icons took {round(end - start, 1)}s")

        return render_template(
            'results.html',
            q=session["query"],
            page=current_page,
            total_pages=len(pages),
            current_page=page_number,
            count=session["count"],
            execution_time=session["duration"]
        )
    except TemplateNotFound:
        logger.error(f"results.html was not found.")
        abort(404)

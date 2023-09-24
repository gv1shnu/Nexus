# Third-party libraries
from flask import Blueprint, abort, render_template, session, request, current_app
from jinja2 import TemplateNotFound

# Internal imports
from src.helpers import get_current_page
from utl.logger import Logger
from src.decl import Pages, Page

res_bp = Blueprint('res', __name__)
logger = Logger()


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


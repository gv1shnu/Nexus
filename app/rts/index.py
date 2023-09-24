# Third-party libraries
from flask import Blueprint, abort, render_template
from jinja2 import TemplateNotFound

# Internal import
from utl.logger import Logger

index_bp = Blueprint('index', __name__)

# Predefined options and filters for the search
OPTIONS: list = [
    "Google", "Bing", "Duckduckgo",
    "Yahoo", "YouTube", "Reddit"
]
FILTERS: list = [
    "Text", "Images",
    "Videos", "News"
]
logger = Logger()


# Home route of the application
@index_bp.route('/')
def index():
    try:
        return render_template(
            "index.html",
            options=OPTIONS,
            filters=FILTERS
        )
    except TemplateNotFound:
        logger.error(f"index.html was not found.")
        abort(404)


@index_bp.route(
    "/in-progress",
    endpoint='progress'
)
def progress():
    try:
        return render_template("in_progress.html")
    except TemplateNotFound:
        logger.error(f"in_progress.html was not found.")
        abort(404)

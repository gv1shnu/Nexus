# Third-party libraries
from flask import Blueprint, abort, render_template, current_app
from jinja2 import TemplateNotFound

# Internal imports
from decl import OPTIONS, FILTERS
from utl.logger import Logger

index_bp = Blueprint('index', __name__)

logger = Logger()


# Home route of the application
@index_bp.route('/')
def index():
    cache_manager = current_app.extensions['cache_manager']
    cache_manager.clear()
    try:
        return render_template(
            "index.html",
            options=OPTIONS,
            filters=FILTERS
        )
    except TemplateNotFound:
        logger.error(f"index.html was not found.")
        abort(404)

# Third-party libraries
from flask import Blueprint, abort, render_template, current_app
from jinja2 import TemplateNotFound

# Internal imports
from decl import OPTIONS, FILTERS, INDEX_TEMPLATE
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
            template_name_or_list=INDEX_TEMPLATE,
            options=OPTIONS,
            filters=FILTERS
        )
    except TemplateNotFound:
        logger.error(f"{INDEX_TEMPLATE} was not found.")
        abort(404)

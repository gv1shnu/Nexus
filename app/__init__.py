
# Python standard library
import os

# Third party libraries
from flask import Flask, request, render_template, abort
from jinja2 import TemplateNotFound

# Internal imports
from app.rts.index import index_bp
from app.act.fetch import fetch_bp
from app.config import Config, basedir
from app.rts.result import res_bp
from decl import MODE, ROUTES
from utl.cache_manager import CacheManager
from utl.logger import Logger

logger = Logger()


# Function that creates flask application and binds with blueprints
def create_app(config_class=Config):
    # Instantiate flask app
    app: Flask = Flask(__name__)

    # Define folder paths
    template_folder: str = os.path.join(basedir, '../tpl')
    static_folder: str = os.path.join(basedir, '../stc')

    # Set app configurations
    app.config.from_object(config_class)
    app.template_folder = template_folder
    app.static_folder = static_folder

    # Defining a custom error handling function to the app
    @app.errorhandler(Exception)
    def handle_error(error):
        # Get current path
        current_route: str = request.path
        if current_route not in ROUTES:
            logger.debug(f"Irrelevant error while fetching {current_route}: {error}")
        else:
            logger.error(f"An error occurred while fetching {current_route} route: {error}")
        if MODE == "DEBUG":
            try:
                # Render a custom error template
                return render_template(
                    "error.html",
                    error_message=str(error)
                )
            except TemplateNotFound:
                logger.error(f"error.html was not found.")
                abort(404)

    cache_manager = CacheManager(app)
    app.extensions['cache_manager'] = cache_manager

    # Registering blueprints with flask app
    app.register_blueprint(index_bp)
    app.register_blueprint(fetch_bp)
    app.register_blueprint(res_bp)

    return app

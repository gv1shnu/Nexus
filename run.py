
# Internal imports
from app import create_app
from utl.logger import Logger

# Third party library
from waitress import serve

MODE = "DEBUG"
logger = Logger()


if __name__ == '__main__':
    app = create_app()
    if MODE == "PRODUCTION":
        serve(app, host='0.0.0.0', port=5000)
    elif MODE == "DEBUG":
        app.run()
    else:
        logger.error("Invalid Mode")
        exit(143)

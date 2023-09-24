# Python standard library
import logging


# Defining a custom formatter for console log
class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[0;37m",  # White
        "INFO": "\033[0;32m",  # Green
        "WARNING": "\033[1;33m",  # Yellow
        "ERROR": "\033[1;31m",  # Red
        "CRITICAL": "\033[1;41m\033[1;37m",  # White text on red background
        "RESET": "\033[0m",  # Reset to default color
    }

    def format(self, record):
        log_message = super().format(record)
        log_level_color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        return f"{log_level_color}{log_message}{self.COLORS['RESET']}"


# Defining a custom logger function
def Logger(log_filename="app.log"):
    logger = logging.getLogger(__name__)
    formatter_string = '%(asctime)s - %(levelname)s - %(filename)s - %(message)s'
    if not logger.handlers:
        logging.basicConfig(level=logging.DEBUG,
                            format=formatter_string,
                            datefmt='%Y-%m-%d %H:%M:%S')
        # Different format for console log
        colored_formatter = ColoredFormatter(formatter_string)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(colored_formatter)
        logger.addHandler(console_handler)

        # Formal format for file log
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(formatter_string)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # To avoid overriding of logging formats of console log to file log and vice-versa.
        logger.propagate = False

    return logger


import logging
import sys
from datetime import datetime
import coloredlogs


def setup_logger():
    logger = logging.getLogger("asterisk_api")
    logger.setLevel(logging.DEBUG)

    # Log format
    log_format = '[%(asctime)s] %(name)s.%(levelname)s: %(message)s'

    # File handler (no colors)
    log_file = f"logs/asterisk_api_{datetime.now().strftime('%Y-%m-%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler (with colors)
    level_styles = {
        'debug': {'color': 'green'},
        'info': {'color': 'blue'},
        'warning': {'color': 'yellow'},
        'error': {'color': 'red'},
        'critical': {'color': 'red', 'bold': True}
    }
    coloredlogs.install(
        level='DEBUG',
        logger=logger,
        fmt=log_format,
        stream=sys.stdout,
        level_styles=level_styles
    )

    return logger

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(log_dir: str = ".logs") -> logging.Logger:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = RotatingFileHandler(
        f"{log_dir}/{datetime.now().strftime('%Y-%m-%d')}.log",
        maxBytes=10**6,
        backupCount=3,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


LOGGER = setup_logger()

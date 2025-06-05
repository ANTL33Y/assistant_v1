import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = os.getenv('LOG_DIR', 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'assistant.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

os.makedirs(LOG_DIR, exist_ok=True)

formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'
)

file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5
)
file_handler.setFormatter(formatter)
file_handler.setLevel(LOG_LEVEL)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(LOG_LEVEL)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    logger.propagate = False
    return logger 
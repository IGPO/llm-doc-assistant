import logging
import os

# Optional: get log level from environment, fallback to INFO
log_level = os.getenv("LOG_LEVEL", "INFO").upper()

logger = logging.getLogger("app")
logger.setLevel(getattr(logging, log_level, logging.INFO))

formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

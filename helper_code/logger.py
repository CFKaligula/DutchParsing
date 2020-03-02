import logging
import os

FORMAT = "%(asctime)s - [%(levelname)s]  %(message)s"

LOG_LEVEL = logging.INFO


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):
        levelname = record.levelname
        return logging.Formatter.format(self, record)


custom_stream_handler = logging.StreamHandler()
formatter = ColoredFormatter(FORMAT)
custom_stream_handler.setFormatter(formatter)

logging.basicConfig(
    level=LOG_LEVEL,
    format=FORMAT,
    handlers=[
        logging.FileHandler(os.path.join('helper_code', 'logger.log')),
        custom_stream_handler
    ])

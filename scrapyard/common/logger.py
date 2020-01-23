import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

import coloredlogs

import settings as default_settings


logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)



def main_logger(settings=default_settings):
    log_dir = os.path.dirname(settings.LOG_FILE_PATH)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    root_logger = logging.getLogger()
    level = getattr(logging, settings.LOG_LEVEL)
    log_formatter = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    filename = datetime.now().strftime('%Y_%m_%d.log')
    filepath = os.path.join(log_dir, filename)

    file_handler = RotatingFileHandler(
        filename=filepath,
        mode='a',
        maxBytes=settings.LOG_MAX_FILE_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT
    )

    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    root_logger.setLevel(level)
    coloredlogs.install(level=level)
    return root_logger


logger = main_logger()

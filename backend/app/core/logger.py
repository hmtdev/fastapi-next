import logging

import sys

from pathlib import Path

from datetime import datetime

# create log file if not exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# log file name
log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"

# log format
log_format = "%(levelname)s:     %(asctime)s - %(message)s"


def setup_logger():
    logger = logging.getLogger("Backend")
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
    )
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()

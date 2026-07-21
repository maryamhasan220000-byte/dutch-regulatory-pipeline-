import sys
from pathlib import Path
import logging 
from logging.handlers import RotatingFileHandler 

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR/"pipeline.log"
MAX_BYTES = 5 * 1024 * 1024
BACKUP_COUNT = 3
LOG_FORMAT =  "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_logger(name: str)-> logging.Logger:

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
     
    if logger.handlers:
        return logger 
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger 
    
 
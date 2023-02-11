import logging
from logging.handlers import TimedRotatingFileHandler

from .settings import BASE_DIR, LOG_LEVEL


LOGS_FOLDER = BASE_DIR / ".data/logs"
LOGS_FOLDER.mkdir(parents=True, exist_ok=True)

FILENAME = "bot.log"
LOG_PATH = LOGS_FOLDER / FILENAME

INTERVAL = 1
INTERVAL_TYPE = "D"
BACKUP_COUNT = 60

FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

handler = TimedRotatingFileHandler(
    LOG_PATH,
    when=INTERVAL_TYPE,
    interval=INTERVAL,
    backupCount=BACKUP_COUNT
)
handler.setFormatter(
    logging.Formatter(FORMAT)
)
handler.setLevel(LOG_LEVEL)

logger = logging.getLogger(__name__)
logger.addHandler(handler)

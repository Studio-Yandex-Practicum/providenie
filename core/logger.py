import logging

from settings import BASE_DIR, LOG_LEVEL

logs_folder = BASE_DIR.parent / '.data/logs'
logs_folder.mkdir(parents=True, exist_ok=True)
filename = 'bot.log'
filnal_dir = logs_folder / filename

logging.basicConfig(
    level=LOG_LEVEL,
    filename=filnal_dir,
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

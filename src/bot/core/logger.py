import logging.config
from pathlib import Path

from bot.constants import key
from bot.core.settings import settings


BASE_DIR = Path(__file__).resolve().parent.parent

LOG_PATH = BASE_DIR / '.data' / 'logs'
LOG_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOG_PATH / settings.log_filename


DEFAULT_LOGGING = {
    'version': 1,
    'disable_exising_loggers': False,
    'formatters': {
        'standard': {
            'format': settings.log_format
        }
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'level': settings.log_level,
            'formatter': 'standard',
        },
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_PATH,
            'when': 'D',
            'interval': 1,
            'backupCount': 60,
            'level': settings.log_level,
            'formatter': 'standard',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': settings.log_level,
            'propagate': True,
        },
    }
}
logging.config.dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger(__name__)


def pydantic_error(field, user_data, error):
    """Reducing the pidantic validation error to a string value."""
    return f'Validation Error in {field} of {user_data[key.FORM][key.DATA].__class__.__name__}: {error}'

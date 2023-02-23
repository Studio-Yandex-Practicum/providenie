import logging
import logging.config

from core import settings


LOG_LEVEL = logging.getLevelName(settings.LOG_LEVEL)

DEFAULT_LOGGING = {
    'version': 1,
    'disable_exising_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s, %(levelname)s, %(name)s, %(message)s'
        },
        'telegram': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'level': 'DEBUG',
            'formatter': 'standard',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'precise',
            'filename': settings.LOG_PATH,
            'maxBytes': 1024,
            'backupCount': 3,
            'level': 'DEBUG',
            'formatter': 'standard',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

logging.config.dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger(__name__)

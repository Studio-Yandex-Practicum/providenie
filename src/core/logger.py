import logging.config

from .settings import LOG_LEVEL, LOG_PATH, LOG_FORMAT

DEFAULT_LOGGING = {
    'version': 1,
    'disable_exising_loggers': False,
    'formatters': {
        'standard': {
            'format': LOG_FORMAT
        }
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'level': LOG_LEVEL,
            'formatter': 'standard',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'precise',
            'filename': LOG_PATH,
            'maxBytes': 1024,
            'backupCount': 5,
            'level': LOG_LEVEL,
            'formatter': 'standard',
        }
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
    }
}

logging.config.dictConfig(DEFAULT_LOGGING)
logger = logging.getLogger(__name__)

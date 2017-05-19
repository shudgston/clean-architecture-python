import logging
import sys
from logging.config import dictConfig
from links.settings import Settings

LOGCONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(name)s -- %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': Settings.LOGGING_LEVEL,
            'stream': sys.stderr,
        },
    #     'file': {
    #         'class': 'logging.handlers.WatchedFileHandler',
    #         'formatter': 'default',
    #         'level': Settings.LOGGING_LEVEL,
    #         'filename': 'tmp.log',
    #     }
    },
    'root': {
        'handlers': ['console'],
        'level': Settings.LOGGING_LEVEL,
    },
}

dictConfig(LOGCONFIG)


def get_logger(name):
    """

    :param name:
    :return:
    """
    return logging.getLogger(name)

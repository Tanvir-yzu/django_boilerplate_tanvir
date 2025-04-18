"""
Logging settings for django_boilerplate_tanvir project.

Must be at the same directory as the settings.py file.

Documentation
https://docs.djangoproject.com/en/3.0/topics/logging/
"""
# PYTHON IMPORTS
import os
# PROJECT IMPORTS
from django_boilerplate_tanvir.local_settings import LOGS_DIR


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {module} {process:d} {thread:d} '
                      '{message}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
    },  # formatters
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',  # Changed to RotatingFileHandler
            'filename': os.path.join(LOGS_DIR, "debug.log"),
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 10,
        },
        'warnings_file': {
            'level': 'WARNING',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',  # Changed to RotatingFileHandler
            'filename': os.path.join(LOGS_DIR, "warnings.log"),
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 10,
        },
    },  # handlers
    'loggers': {
        '': {  # root logger
            'handlers': ['console', 'file', 'warnings_file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO').upper(),
        },
        'customauth': {
            'handlers': ['console', 'file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG').upper(),
            'propagate': False,  # required to eliminate duplication on root
        },
        'dashboard': {
            'handlers': ['console', 'file', 'warnings_file'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG').upper(),
            'propagate': False,
        },
        # 'app_name': {
        #     'handlers': ['console', 'file'],
        #     'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG').upper(),
        #     'propagate': False,  # required to eliminate duplication on root
        # },
    },  # loggers
}  # logging
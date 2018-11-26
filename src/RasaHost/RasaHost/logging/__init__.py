from logging import StreamHandler
import logging
from RasaHost.database import *
import datetime
from flask import request, has_request_context
import flask
import traceback
import coloredlogs
import re
import uuid

__all__ = ['LoggingDbHandler', 'LoggingFilter', 'LoggingSocketioHandler', 'get_request_id', 'get_sender_id', 'set_sender_id']

from RasaHost.logging.db_handler import LoggingDbHandler
from RasaHost.logging.filter import LoggingFilter
from RasaHost.logging.socketio_handler import LoggingSocketioHandler
from RasaHost.logging.request_id import get_request_id
from RasaHost.logging.sender_id import get_sender_id, set_sender_id

log_level = 'DEBUG'

def enable():
    field_styles = coloredlogs.DEFAULT_FIELD_STYLES.copy()
    field_styles['asctime'] = {}
    level_styles = coloredlogs.DEFAULT_LEVEL_STYLES.copy()
    level_styles['debug'] = {}
    coloredlogs.install(
                level=log_level,
                use_chroot=False,
                fmt='%(asctime)s %(levelname)-8s %(name)s  - %(message)s',
                level_styles=level_styles,
                field_styles=field_styles)
        
    dbHandler = LoggingDbHandler()
    dbHandler.setLevel(log_level)
    logging.getLogger().addHandler(dbHandler)
    logging.getLogger().addHandler(logging.FileHandler("logs.txt"))
    #logging.getLogger('werkzeug').addHandler(dbHandler)
    #socketio logging
    #logging.getLogger().addHandler(LoggingSocketioHandler())
    #file logging
    
        

    for handler in logging.getLogger().handlers:
        handler.setLevel(log_level)
        handler.addFilter(LoggingFilter())
        #handler.setFormatter(logging.Formatter("[%(sender_id)s] [%(asctime)s] [%(name)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

    import requests.api
    def my_get(url, **kwargs):
        print('Hello World!')
        kwargs.setdefault('allow_redirects', True)
        return requests.api.request('get', url, **kwargs)
    requests.api.get = my_get

    def my_post(url, **kwargs):
        print('Hello World!')
        kwargs.setdefault('allow_redirects', True)
        return requests.api.request('post', url, **kwargs)
    requests.api.post = my_post
        #logging.getLogger('socketio').setLevel(logging.INFO)
        #logging.getLogger('engineio').setLevel(logging.INFO)
        #logging.getLogger('werkzeug').setLevel(logging.INFO)

def set_log_level(self, log_level):
    self.log_level = log_level
    for handler in logging.getLogger().handlers:
        handler.setLevel(log_level)


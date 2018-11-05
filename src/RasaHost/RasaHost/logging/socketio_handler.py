import logging
from logging import StreamHandler
from RasaHost.database import *
import datetime
from flask import request, has_request_context
import flask
import traceback
import coloredlogs
import re
import uuid


class LoggingSocketioHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self)
    def emit(self, record):
        import sys
        from RasaHost import host
        try:
            host.socketio.emit('console', {'log_level': record.levelname, 'message': record.getMessage()})
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            print(e)
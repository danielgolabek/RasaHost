#from rasa_core import utils
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

class LoggingService:
    def __init__(self):
        self.log_level = 'DEBUG'
    def initialize(self):
        #coloredlogs

        field_styles = coloredlogs.DEFAULT_FIELD_STYLES.copy()
        field_styles['asctime'] = {}
        level_styles = coloredlogs.DEFAULT_LEVEL_STYLES.copy()
        level_styles['debug'] = {}
        coloredlogs.install(
                level=self.log_level,
                use_chroot=False,
                fmt='%(asctime)s %(levelname)-8s %(name)s  - %(message)s',
                level_styles=level_styles,
                field_styles=field_styles)
        #db logging
        dbHandler = LoggingDbHandler()
        dbHandler.setLevel(self.log_level)
        logging.getLogger().addHandler(dbHandler)
        #logging.getLogger('werkzeug').addHandler(dbHandler)
        #socketio logging
        logging.getLogger().addHandler(LoggingSocketioHandler())
        #file logging
        logging.getLogger().addHandler(logging.FileHandler("logs.txt"))
        

        for handler in logging.getLogger().handlers:
            handler.setLevel(self.log_level)
            handler.addFilter(LoggingSenderIdFilter())
            #handler.setFormatter(logging.Formatter("[%(sender_id)s] [%(asctime)s] [%(name)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

        #logging.getLogger('socketio').setLevel(logging.INFO)
        #logging.getLogger('engineio').setLevel(logging.INFO)
        #logging.getLogger('werkzeug').setLevel(logging.INFO)

    def set_log_level(self, log_level):
        self.log_level = log_level
        for handler in logging.getLogger().handlers:
            handler.setLevel(log_level)

    def find(self, query):
        return DbContext().logs.find(query)


class LoggingDbHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self)
    def emit(self, record):
        log = Log(
            name = record.name, 
            module = record.module,
            filename = record.filename,
            line_no = record.lineno,
            log_level = record.levelname,
            message = record.getMessage(),
            exception = traceback.print_exception(*record.exc_info) if record.exc_info else None,
            created = datetime.datetime.fromtimestamp(record.created),
            sender_id = record.sender_id,
            request_id = record.request_id
            )
        domainContext = DbContext()
        domainContext.logs.save(log)
        domainContext.commit()

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


class LoggingSenderIdFilter(logging.Filter):
    def request_id(self):
        if getattr(flask.g, 'request_id', None):
            return flask.g.request_id
        original_request_id = flask.request.headers.get("X-Request-Id")
        request_id = original_request_id if original_request_id else str(uuid.uuid4())
        flask.g.request_id = request_id
        return flask.g.request_id

    def filter(self, record):
        if has_request_context():
            record.sender_id = request.view_args['sender_id'] if request.view_args and 'sender_id' in request.view_args else None
            if not record.sender_id:
                record.sender_id = request.json['sender_id'] if request.json  and 'sender_id' in request.json else None
            record.request_id = self.request_id()
        else:
            record.sender_id = next(iter(re.findall("/conversations/(.*)/[a-zA-Z]", record.getMessage())), None)
            record.request_id = None
        return True
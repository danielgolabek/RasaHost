#from rasa_core import utils
import logging
from logging import StreamHandler
from RasaHost.database import *
import datetime
from flask import request, has_request_context
import traceback
import coloredlogs

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
            sender_id = record.sender_id
            )
        domainContext = DbContext()
        domainContext.logs.save(log)
        domainContext.commit()

class LoggingSocketioHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self)
    def emit(self, record):
        from RasaHost import socketio
        import sys
        try:
             socketio.emit('console', {'log_level': record.levelname, 'message': record.getMessage()})
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            print(e)
       


class LoggingSenderIdFilter(logging.Filter):
    def filter(self, record):
        if has_request_context():
            record.sender_id = request.view_args['sender_id'] if 'sender_id' in request.view_args else None
            if not record.sender_id:
                record.sender_id = request.json['sender_id'] if 'sender_id' in request.json else None
        else:
            record.sender_id = None
        return True

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
        #socketio logging
        logging.getLogger().addHandler(LoggingSocketioHandler())
        #file logging
        logging.getLogger().addHandler(logging.FileHandler("logs.txt"))
        

        for handler in logging.getLogger().handlers:
            handler.setLevel(self.log_level)
            handler.addFilter(LoggingSenderIdFilter())
            #handler.setFormatter(logging.Formatter("[%(sender_id)s] [%(asctime)s] [%(name)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

        logging.getLogger('socketio').setLevel(logging.ERROR)
        logging.getLogger('engineio').setLevel(logging.ERROR)
        logging.getLogger('werkzeug').setLevel(logging.ERROR)

    def set_log_level(self, log_level):
        self.log_level = log_level
        for handler in logging.getLogger().handlers:
            handler.setLevel(log_level)

    def find(self, query):
        return DbContext().logs.find(query)

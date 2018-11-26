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
            exception = "".join(traceback.format_exception(*record.exc_info)) if record.exc_info else None,
            created = datetime.datetime.fromtimestamp(record.created),
            sender_id = record.sender_id if record.sender_id else None,
            request_id = record.request_id if record.request_id else None
            )
        domainContext = DbContext()
        domainContext.logs.save(log)
        domainContext.commit()
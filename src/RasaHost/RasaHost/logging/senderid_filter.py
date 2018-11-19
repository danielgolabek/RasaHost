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
from RasaHost.logging.request_id import get_request_id


class LoggingSenderIdFilter(logging.Filter):
    def filter(self, record):
        try:
            record.sender_id = None
            record.request_id = None
            if has_request_context():
                record.sender_id = request.view_args['sender_id'] if request and request.view_args and 'sender_id' in request.view_args else None
                if not record.sender_id:
                    record.sender_id = request.json['sender_id'] if request and request.json  and 'sender_id' in request.json else None
                record.request_id = get_request_id()
            else:
                record.sender_id = next(iter(re.findall("/conversations/(.*)/[a-zA-Z]", record.getMessage())), None)
                record.request_id = None
        except:
            return True
        return True
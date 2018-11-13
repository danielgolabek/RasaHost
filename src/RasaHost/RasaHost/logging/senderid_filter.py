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


class LoggingSenderIdFilter(logging.Filter):
    def request_id(self):
        if getattr(flask.g, 'request_id', None):
            return flask.g.request_id
        original_request_id = flask.request.headers.get("X-Request-Id")
        request_id = original_request_id if original_request_id else str(uuid.uuid4())
        flask.g.request_id = request_id
        return flask.g.request_id

    def filter(self, record):
        try:
            record.sender_id = None
            record.request_id = None
            if has_request_context():
                record.sender_id = request.view_args['sender_id'] if request and request.view_args and 'sender_id' in request.view_args else None
                if not record.sender_id:
                    record.sender_id = request.json['sender_id'] if request and request.json  and 'sender_id' in request.json else None
                record.request_id = self.request_id()
            else:
                record.sender_id = next(iter(re.findall("/conversations/(.*)/[a-zA-Z]", record.getMessage())), None)
                record.request_id = None
        except:
            return True
        return True
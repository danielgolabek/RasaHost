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

def get_request_id():
    if has_request_context():
        if getattr(flask.g, 'request_id', None):
            return flask.g.request_id
        original_request_id = flask.request.headers.get("X-Request-Id")
        request_id = original_request_id if original_request_id else str(uuid.uuid4())
        flask.g.request_id = request_id
        return flask.g.request_id
    else:
        return None

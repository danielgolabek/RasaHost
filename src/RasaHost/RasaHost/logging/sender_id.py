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

def get_sender_id(message = None):
    if has_request_context():
        if getattr(flask.g, 'sender_id', None):
            return flask.g.sender_id
        sender_id = request.view_args['sender_id'] if request and request.view_args and 'sender_id' in request.view_args else None
        if sender_id:
            return sender_id
        sender_id = request.json['sender_id'] if request and request.json  and 'sender_id' in request.json else None
        return sender_id
    else:
        if message:
            return next(iter(re.findall("/conversations/(.*)/[a-zA-Z]", message)), None)
        else:
            return None

def set_sender_id(sender_id):
    if has_request_context():
        flask.g.sender_id = sender_id
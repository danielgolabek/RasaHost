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
        pass

    def find(self, query):
        return DbContext().logs.find(query)



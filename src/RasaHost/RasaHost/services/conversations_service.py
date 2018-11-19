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
from RasaHost.logging import get_request_id

class ConversationsService:
    def __init__(self):
        pass

    def find(self, query):
        return DbContext().conversations.find(query)

    def save(self, sender_id, request, response):
        conversation = Conversation()
        conversation.request = request
        conversation.response = response
        conversation.sender_id = sender_id
        conversation.request_id = get_request_id()
        conversation.created = datetime.datetime.utcnow()
        DbContext().conversations.save(conversation)



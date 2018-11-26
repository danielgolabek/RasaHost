#from rasa_core import utils
import logging
from logging import StreamHandler
from RasaHost.database import *
import datetime
from flask import request, has_request_context
import flask
import sys
import traceback
import coloredlogs
import re
import uuid
import json
from RasaHost.logging import get_request_id, set_sender_id
from RasaHost import host

import logging
logger = logging.getLogger(__name__)

class ConversationsService:
    def __init__(self):
        pass

    def find(self, query):
        return DbContext().conversations.find(query)

    def save(self, sender_id, request, response, response_raw):
        conversation = Conversation()
        conversation.request = request
        conversation.response = response
        conversation.response_raw = response_raw
        conversation.sender_id = sender_id
        conversation.request_id = get_request_id()
        conversation.created = datetime.datetime.utcnow()
        DbContext().conversations.save(conversation)

   
    def handle_message(self, *args, **kwargs):
            message = None
            text = None
            sender_id = None

            try:
                message = next(iter(args))
                if message:
                    text = message.text
                    sender_id = message.sender_id
                    set_sender_id(sender_id)
            except:
                e = "\n". join(traceback.format_exception(*sys.exc_info()))
                logger.error(e)

            send_proxy = None
            try:
                
                if message and message.output_channel:
                    send_proxy = SendProxy(message.output_channel.send)
                    message.output_channel.send = send_proxy.send

                output = host.agent.handle_message(*args, **kwargs) or (send_proxy.output if send_proxy else [])

                response = [(x["text"] if "text" in x else None) for x in output]
                response_raw = [{"text":x.get("text")} for x in output]

                self.save(sender_id=sender_id, 
                          request=text, 
                          response=json.dumps(response), 
                          response_raw=json.dumps(response_raw))

                return output
            except:
                e = "\n".join(traceback.format_exception(*sys.exc_info()))
                output = (send_proxy.output if send_proxy else [])
                response = [(x["text"] if "text" in x else None) for x in output]
                if len(response) == 0:
                    response = e
                response_raw = {}
                response_raw["output"] = [{"text":x.get("text")} for x in output]
                response_raw["error"] = e
                logger.error(e)
                self.save(sender_id=sender_id, 
                          request=message, 
                          response=json.dumps(response), 
                          response_raw=json.dumps(response_raw))
                raise

    def handle_text(self, message, sender_id=None):
        try:
            output = host.agent.handle_text(message, sender_id=sender_id)
        
            response = [(x["text"] if "text" in x else None) for x in output]
            response_raw = [{"text":x.get("text")} for x in output]
            self.save(sender_id = sender_id, 
                      request = message, 
                      response = json.dumps(response), 
                      response_raw = json.dumps(response_raw))

            return output
        except:
            e = "\n".join(traceback.format_exception(*sys.exc_info()))
            response_raw = {}
            response_raw["error"] = e
            logger.error(e)
            self.save(sender_id=sender_id, 
                      request=message, 
                      response=e, 
                      response_raw=json.dumps(response_raw))
            raise


class SendProxy:
    def __init__(self, send):
        self.orginal_send = send
        self.output = None
        pass

    def send(self, *args, **kwargs):
        self.output = [x for x in args if isinstance(x, dict)]
        return self.orginal_send(*args, **kwargs)

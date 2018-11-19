"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json
import logging
import sys
import traceback
import json
from RasaHost import host
app = host.flask
from RasaHost.services import *
from RasaHost.database import *

logger = logging.getLogger(__name__)

@app.route("/conversations/<sender_id>/respond")
def rasa_respond(sender_id):
    message = None
    try:
        if 'query' in request.args:
            message = request.args.get('query')
        elif 'q' in request.args:
            message = request.args.get('q')
        
        output = host.agent.handle_text(message, sender_id=sender_id)
        
        text = json.dumps([(x["text"] if "text" in x else None) for x in output])
        raw = json.dumps([{"text":x.get("text")} for x in output])
        ConversationsService().save(sender_id = sender_id, request = message, response = text, response_raw = raw)

        response = jsonify(output)
        return response
    except:
        e = "\n". join(traceback.format_exception(*sys.exc_info()))
        logger.error(e)
        ConversationsService().save(sender_id=sender_id, request=message, response=e, response_raw=json.dumps({"error": e}))
        response = jsonify({"error": e})
        response.status_code = 400
        return response


@app.route("/conversations/<sender_id>/parse")
def rasa_parse(sender_id):
    try:
        if 'query' in request.args:
            message = request.args.get('query')
        elif 'q' in request.args:
            message = request.args.get('q')

        output = host.agent.start_message_handling(message, sender_id=sender_id)
        return jsonify(output)
    except:
        e = "\n". join(traceback.format_exception(*sys.exc_info()))
        logger.error(e)
        response = jsonify({"error": e})
        return response

@app.route("/actions", methods = ['GET', 'POST'])
def actions():
    action_call = request.json
    try:
        response = host.actionExecutor.run(action_call)
        return jsonify(response)
    except:
        e = "\n". join(traceback.format_exception(*sys.exc_info()))
        logger.error(e)
        response = jsonify({"error": e, "action_name": action_call})
        response.status_code = 400
        return response

    
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json

from RasaHost import host
app = host.flask
from RasaHost.services import *
from RasaHost.database import *

@app.route('/logs/all')
def logs_all():
    return render_template(
        'logs/all.html',
        title='Logs - all',
    )

@app.route('/logs/conversations')
def logs_conversations():
    return render_template(
        'logs/conversations.html',
        title='Logs - conversations',
    )

@app.route('/logs/console')
def logs_console():
    return render_template(
        'logs/console.html',
        title='Logs - console',
    )


@app.route('/api/logs/all', methods=['GET'])
def api_logs_all():
    query = request.args.get('q')
    page = int(request.args.get('p'))
    pageCount = 200
    logs = [
        {
        'created': f"{l.created:%Y-%m-%d %H:%M:%S}",
        'sender_id': l.sender_id, 
        'request_id': l.request_id, 
        'name': l.name,
        'module': l.module,
        'filename': l.filename,
        'line_no': l.line_no,
        'log_level': l.log_level,
        'message': l.message,
        'exception': l.exception
        } for l in DbContext().logs.find(query, page, pageCount)]

    return jsonify({'results': logs})

@app.route('/api/logs/conversations', methods=['GET'])
def api_logs_conversations():
    query = request.args.get('q')
    page = int(request.args.get('p'))
    pageCount = 200
    conversations = DbContext().logs.find_conversations(query, page, pageCount)

    logs = [
        {
        'created': f"{l.created:%Y-%m-%d %H:%M:%S}",
        'sender_id': l.sender_id, 
        'request_id': l.request_id, 
        'name': l.name,
        'module': l.module,
        'filename': l.filename,
        'line_no': l.line_no,
        'log_level': l.log_level,
        'message': l.message,
        'exception': l.exception
        } for l in DbContext().logs.find_conversations(query, page, pageCount)]

    return jsonify({'results': logs})


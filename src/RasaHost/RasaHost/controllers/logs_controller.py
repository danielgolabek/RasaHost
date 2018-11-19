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

@app.route('/logs/rasa')
def logs_rasa():
    return render_template(
        'logs/rasa.html',
        title='Logs - rasa',
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

@app.route('/api/logs/rasa', methods=['GET'])
def api_logs_rasa():
    query = request.args.get('q')
    page = int(request.args.get('p'))
    pageCount = 100
    
    logs_list = DbContext().logs.find_rasa(query, page, pageCount)
    logs_grouped = {}
    for log in logs_list:
        if not log.request_id in logs_grouped:
            logs_grouped[log.request_id] = []
        logs_grouped[log.request_id].append({
            'created': f"{log.created:%Y-%m-%d %H:%M:%S}",
            'sender_id': log.sender_id, 
            'request_id': log.request_id, 
            'name': log.name,
            'module': log.module,
            'filename': log.filename,
            'line_no': log.line_no,
            'log_level': log.log_level,
            'message': log.message,
            'exception': log.exception
            })
    logs_grouped_list = []
    for key, value in logs_grouped.items():
            logs_grouped_list.append(value)
    
    return jsonify({'results': logs_grouped_list})

@app.route('/api/logs/conversations', methods=['GET'])
def api_logs_conversations():
    query = request.args.get('q')
    page = int(request.args.get('p'))
    pageCount = 200
    conversations = DbContext().conversations.find(query, page, pageCount)
    results = [
        {
        'created': f"{x.created:%Y-%m-%d %H:%M:%S}" if x.created else "",
        'sender_id': x.sender_id, 
        'request_id': x.request_id, 
        'request': x.request,
        'response': x.response,
        } for x in conversations]

    return jsonify({'results': results})
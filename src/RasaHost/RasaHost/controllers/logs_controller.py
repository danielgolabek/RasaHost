"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json

from RasaHost import app
from RasaHost.services import *
from RasaHost.database import *

@app.route('/logs/history')
def logs_history():
    return render_template(
        'logs/history.html',
        title='Logs - history',
    )

@app.route('/logs/console')
def logs_console():
    return render_template(
        'logs/console.html',
        title='Logs - console',
    )


@app.route('/api/logs/history', methods=['GET'])
def api_logs_history():
    q = request.args.get('q')
    logs = [
        {
        'created': f"{l.created:%Y-%m-%d %H:%M:%S}",
        'sender_id': l.sender_id, 
        'name': l.name,
        'module': l.module,
        'filename': l.filename,
        'line_no': l.line_no,
        'log_level': l.log_level,
        'message': l.message,
        'exception': l.exception
        } for l in DbContext().logs.find(q)]
    return jsonify(logs)
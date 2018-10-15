"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json

from RasaHost import host
app = host.flask
from RasaHost.services import *

@app.route('/domain')
def domain():
    model={'text': DomainService().get_text()}
    return render_template(
        'domain/domain.html',
        title='Domain',
        model=model,
        model_json=json.dumps(model)
    )

@app.route('/domain/edit')
def domain_edit():
    model={'text': DomainService().get_text()}
    return render_template(
        'domain/edit.html',
        title='Domain',
        model=model,
        model_json=json.dumps(model)
    )

@app.route('/api/domain', methods=['GET'])
def api_domain_get():
    model={'text': DomainService().get_text()}
    return model

@app.route('/api/domain', methods=['POST', 'PUT'])
def api_domain_post():
    text = request.json['text']
    DomainService().update_text(text)
    return jsonify({'result': {'text': text}})

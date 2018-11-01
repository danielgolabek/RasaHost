"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json

from RasaHost import host
app = host.flask
from RasaHost.services import *

@app.route('/analyze')
def analyze():
    model=AnalyzeService().analyze()
    return render_template(
        'analyze/index.html',
        title='Domain',
        model=model,
        model_json=json.dumps(model)
    )

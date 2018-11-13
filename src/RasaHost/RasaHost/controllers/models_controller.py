"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json
import zlib
import base64

from RasaHost import host
app = host.flask
from RasaHost.services import *

@app.route('/models/MemoizationPolicy')
def models_memoization_policy():
    return render_template(
        'models/memoization_policy.html',
        title='MemoizationPolicy',
    )

@app.route('/api/models/MemoizationPolicy/lookups/decode', methods=['POST'])
def api_models_memoization_policy_lookups_decode():
    MemoizationPolicyService('C:\\Projects\\GSA\\Investec.Bot\\Investec.Bot\\models\\current\\dialogue\\policy_1_MemoizationPolicy').decode()
    return jsonify({"result":"ok"})


@app.route('/api/models/MemoizationPolicy/lookups', methods=['GET'])
def api_models_memoization_policy_lookups():
    query = request.args.get('q')
    last_index = int(request.args.get('i', 0))
    result = MemoizationPolicyService('C:\\Projects\\GSA\\Investec.Bot\\Investec.Bot\\models\\current\\dialogue\\policy_1_MemoizationPolicy').find(query, last_index)
    return jsonify({"result": result})

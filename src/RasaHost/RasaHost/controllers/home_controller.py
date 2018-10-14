"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json

from RasaHost import app
from RasaHost.models import PollNotFound
from RasaHost.models.factory import create_repository
from RasaHost.settings import REPOSITORY_NAME, REPOSITORY_SETTINGS
from RasaHost.services import *


repository = create_repository(REPOSITORY_NAME, REPOSITORY_SETTINGS)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page, with a list of all polls."""
    return render_template(
        'home/index.html',
        title='Home',
        year=datetime.now().year,
        polls=repository.get_polls(),
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'home/contact.html',
        title='Contact',
        year=datetime.now().year,
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'home/about.html',
        title='About',
        year=datetime.now().year,
        repository_name=repository.name,
    )

@app.errorhandler(PollNotFound)
def page_not_found(error):
    """Renders error page."""
    return 'Page does not exist.', 404

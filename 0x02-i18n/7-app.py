#!/usr/bin/env python3
"""implimentaion of flask app"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import (Any, Dict)
import pytz


class Config:
    """default languages"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Any:
    """return a user dictionary or none"""
    if request.args.get('login_as'):
        login_id = int(request.args.get('login_as'))
        if login_id in users:
            return users.get(login_id)
    return None


@app.before_request
def before_request() -> None:
    """find a user"""
    g.user = get_user()


@app.route('/')
def single() -> str:
    """renders a single html helloworld"""
    return render_template('5-index.html')


@babel.localeselector
def get_locale() -> str:
    """selects the appropriate locale"""
    locale_from_url = request.args.get('locale')
    if locale_from_url and locale_from_url in app.config['LANGUAGES']:
        return locale_from_url

    if g.user and 'locale' in g.user and g.user['locale'] \
            in app.config['LANGUAGES']:
        return g.user['locale']

    request_locale = request.accept_languages.best_match(
        app.config['LANGUAGES'])
    if request_locale:
        return request_locale

    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone():
    """gets the timezone of user"""
    timezone = request.args.get('timezone', '').strip()
    if not timezone and g.user:
        timezone = g.user['timezone']

    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


if __name__ == '__main__':
    app.run(debug=True)

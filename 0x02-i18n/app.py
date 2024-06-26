#!/usr/bin/env python3
"""implimentaion of flask app"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _, format_time
from babel import numbers
from datetime import datetime
from typing import (Any, Dict)
from pytz import timezone
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
def home():
    """renders a single html helloworld"""
    logged_in_as = _("logged_in_as", username=g.user["name"]) \
        if g.user else None
    not_logged_in = _("not_logged_in")
    home_header = _("home_header")
    home_title = _("home_title")
    tz = str(get_timezone())
    print(f"tz is {tz}")
    
    time = pytz.timezone(tz)
    time_now = format_time(datetime.now(time))
    current_time = _("current_time_is", current_time=str(time_now))
    print(f"time now is  {current_time}")
    return render_template(
        '7-index.html',
        home_header=home_header,
        home_title=home_title,
        logged_in_as=logged_in_as,
        not_logged_in=not_logged_in,
        current_time=current_time
    )


@babel.localeselector
def get_locale():
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
    user_timezone = request.args.get('timezone', '').strip()
    if not user_timezone:
        user_timezone = g.user['timezone'] if g.user else "UTC"
    try:
        timezone(user_timezone)        
        return user_timezone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


if __name__ == '__main__':
    app.run(debug=True)

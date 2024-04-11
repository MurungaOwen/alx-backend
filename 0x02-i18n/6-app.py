#!/usr/bin/env python3
"""implimentaion of flask app"""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
from typing import (Any, Dict)


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
    """renders a logged in user"""
    logged_in_as = _("logged_in_as", username=g.user["name"]) \
        if g.user else None
    not_logged_in = _("not_logged_in")
    home_header = _("home_header")
    home_title = _("home_title")

    return render_template(
        '6-index.html',
        home_header=home_header,
        home_title=home_title,
        logged_in_as=logged_in_as,
        not_logged_in=not_logged_in
    )


@babel.localeselector
def get_locale() -> str:
    """selects the appropriate locale"""
    locale_from_url = request.args.get('locale')
    if locale_from_url and locale_from_url in app.config['LANGUAGES']:
        return locale_from_url

    user = get_user()
    print(f"user locale is {user['locale']}")
    if user['locale'] in app.config["LANGUAGES"]:
        return user['locale']

    request_locale = request.accept_languages.best_match(
        app.config['LANGUAGES'])
    if request_locale:
        return request_locale

    return app.config['BABEL_DEFAULT_LOCALE']


if __name__ == '__main__':
    app.run(debug=True)

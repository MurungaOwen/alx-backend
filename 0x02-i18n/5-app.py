#!/usr/bin/env python3
"""
flask app
"""
from flask import Flask, request, g, render_template
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)


# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id):
    """get user based on id"""
    return users.get(user_id)


@app.before_request
def before_request():
    """
    run before all
    """
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None


def get_locale():
    user_locale = None
    if g.user:
        user_locale = g.user.get('locale')
    return user_locale if user_locale in ['en', 'fr'] else 'en'


@app.route('/')
def index():
    """
    home page
    """
    logged = _('logged_in_as %(username)s', username=g.user['name'])
    not_logged = _('not_logged_in')
    return render_template(
        '5-index.html', logged=logged, not_logged=not_logged)


if __name__ == '__main__':
    app.run(debug=True)

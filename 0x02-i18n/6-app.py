#!/usr/bin/env python3
"""
flask app
"""
from flask import request, g, Flask, render_template
from flask_babel import Babel, _


app = Flask(__name__)
babel = Babel(app)

LOCALES = ['en', 'fr']


def get_locale():
    locale = request.args.get('locale')
    if locale in LOCALES:
        return locale

    if g.user and 'locale' in g.user and g.user['locale'] in LOCALES:
        return g.user['locale']

    locale = request.headers.get('Accept-Language')
    if locale:
        for lang in locale.replace('-', '_').split(','):
            lang = lang.split(';')[0]
            if lang in LOCALES:
                return lang

    return 'en'


@app.before_request
def before_request():
    users = {
        1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
        2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
        3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
        4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
    }

    user_id = int(request.args.get('login_as', 0))
    g.user = users.get(user_id)


@app.route('/')
def index():
    """
    home page
    """
    logged = _('logged_in_as %(username)s', username=g.user['name'])
    not_logged = _('not_logged_in')
    return render_template(
        '6-index.html', logged=logged, not_logged=not_logged)


if __name__ == '__main__':
    app.run(debug=True)

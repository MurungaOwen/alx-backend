#!/usr/bin/env python3
"""
flask app
"""
from flask import request, Flask, render_template
from flask_babel import Babel, _, force_locale


app = Flask(__name__)


class Config:
    """configure languages"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


babel = Babel(app)
app.config.from_object(Config)


@babel.localeselector
def get_locale() -> str:
    """force locale to france"""
    return "fr"


@app.route("/")
@force_locale("fr")
def home():
    """home page"""
    home_title = _("Welcome to Holberton")
    home_header = _("Hello world!")
    return render_template(
        "3-index.html",home_title = home_title,
        home_header = home_header
    )


if __name__ == '__main__':
    app.run()

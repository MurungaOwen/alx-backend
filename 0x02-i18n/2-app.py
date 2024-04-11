#!/usr/bin/env python3
"""
flask app
"""
from flask import request, Flask, render_template
from flask_babel import Babel


app = Flask(__name__)


class Config:
    """configure languages"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


babel = Babel(app)
app.config.from_object(Config)


@app.route("/")
def home() -> str:
    """home page"""
    return render_template("2-index.html")


@babel.localeselector
def get_locale():
    """get specific locale of user"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == '__main__':
    app.run()

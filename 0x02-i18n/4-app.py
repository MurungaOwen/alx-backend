#!/usr/bin/env python3
"""implimentaion of flask app"""
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """default languages"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@app.route('/')
def single():
    """renders a single html helloworld"""
    return render_template('4-index.html')


@babel.localeselector
def get_locale():
    """selects the appropriate locale"""
    local = request.args.get('locale')
    if local in app.config['LANGUAGES']:
        return local
    return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == '__main__':
    app.run(debug=True)

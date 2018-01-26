import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_cors import CORS
from flask_seasurf import SeaSurf
from flask_mobility import Mobility
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


if 'FLASK_APP_SETTINGS' in os.environ:
    app.config.from_envvar('FLASK_APP_SETTINGS')
else:
    app.config.from_object('agoricco.default_settings')

app.config['BABEL_DEFAULT_LOCALE'] = 'fr'
#user.locale = 'fr'

csp = {
    'default-src': [
        '\'self\'',
    ],
    'img-src': '*',
    'media-src': '*.cloudfront.net',
    'script-src': [
        '\'self\'',
        'agoric.co',
        'www.google-analytics.com',
        'www.googletagmanager.com',
        'code.jquery.com',
        'cdnjs.cloudflare.com',
        'cdn.steemjs.com',
    ],
    'style-src': [
        '\'self\'',
        'agoric.co',
        'hello.myfonts.net',
    ],
    'font-src': [
        '\'self\'',
        'agoric.co',
        'hello.myfonts.net',
    ],
    'connect-src': [
        '\'self\'',
        'cdn.steemjs.com',
    ],
}
Talisman(app, content_security_policy=csp)
db = SQLAlchemy(app)

cors = CORS(app, resources={r"/static/webfonts/*": {"origins": "*"}})
csrf = SeaSurf(app)
Mobility(app)

import agoricco.models
import agoricco.views

if __name__ == "__main__":
    app.run(host='0.0.0.0')

<<<<<<< HEAD
# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from flask import jsonify, make_response
from flask_jwt_extended import fresh_jwt_required
=======
import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
>>>>>>> d3c274b57f6102f820b377efbc00e4c8d07dc009

app = Flask(__name__)
CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

db = SQLAlchemy(app)

<<<<<<< HEAD
jwt = JWTManager(app)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

bcrypt = Bcrypt(app)

from project.server.api.auth import bp_auth  # noqa
app.register_blueprint(bp_auth)

from project.server.api.auth.services.token_blacklist import register_headers  # noqa
register_headers(jwt)


# Make sure the sqlalchemy database is created
@app.before_first_request
def setup_sqlalchemy():
    db.create_all()


@app.route('/')
@fresh_jwt_required
def index():
    response_object = {
        'status': 'success',
        'message': 'Deu certo, você conseguiu entrar'
    }
    return make_response(jsonify(response_object)), 200
=======
bcrypt = Bcrypt(app)

from project.server.auth.views import auth_blueprint # noqa
app.register_blueprint(auth_blueprint)
>>>>>>> d3c274b57f6102f820b377efbc00e4c8d07dc009

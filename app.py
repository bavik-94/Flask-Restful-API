import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, get_jwt_identity

from db import db

from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Items, Item
from resources.store import Stores, Store
from blacklist import _blacklist

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'teddy-bear'
api = Api(app)

jwt = JWTManager(app)  # not creating /auth endpoint


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in _blacklist


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # instead of hard-coding, use config or database
        return {'is_admin': True}
    return {'is_admin':  False}


@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return jsonify(code="dave", err="I can't let you do that"), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'message': 'Invalid Token'}), 401


@jwt.unauthorized_loader
def unauthorized_loader_callback(message):
    return jsonify({'message': message}), 401


@jwt.needs_fresh_token_loader
def need_fresh_token_callback():
    return jsonify({'message': 'Need fresh token'}), 401


@jwt.revoked_token_loader
def my_revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'token revoked'}), 401


api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Stores, '/stores')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000)


import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Items, Item
from resources.store import Stores, Store


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'teddy-bear'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth endpoint


api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Stores, '/stores')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(port=5000)


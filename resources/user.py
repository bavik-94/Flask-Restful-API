import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank"
                        )

    def post(self):
        req = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(req['username'])

        if user:
            return {'message': 'User already exists'}, 401
        else:
            user = UserModel(**req)
            UserModel.register(user)
            return {'message': 'User Registered'}, 200

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Stores(Resource):
    @staticmethod
    def get():
        return StoreModel.get_all_stores()


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be blank"
                        )

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return store.get_all_items()
        return {"message": "Store not Found"}

    @staticmethod
    def post(name):
        item = StoreModel.find_store_by_name(name)

        if item:
            return {'message': 'Store Already Exists'}, 400
        else:
            new_item = StoreModel(name)
            new_item.save_to_db()
            return {'message': 'Store Created'}, 200

    @staticmethod
    def put(name):
        store = StoreModel.find_store_by_name(name)
        if store:
            store.name = name
            store.save_to_db()
            return {'message': 'Store Updated'}, 200
        else:
            new_store = StoreModel(name)
            new_store.save_to_db()
            return {'message': 'Store Created'}, 200


    @staticmethod
    def delete(name):
        store = StoreModel.find_store_by_name(name)

        if store:
            store.delete()
            return {'message': 'Store Deleted'}, 200
        else:
            return {'message': 'Store not Found'}, 200
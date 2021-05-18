from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from models.item import ItemModel


class Items(Resource):
    @jwt_required(optional=True)
    def get(self):  # change output if JWT is present
        user_id = get_jwt_identity()
        if user_id:
            return ItemModel.get_all_items(full=True)
        else:
            return ItemModel.get_all_items(full=False)


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field cannot be blank",

                        )
    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="This field cannot be blank",

                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json(), 200
        return {"message": "Item not Found"}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        req = Item.parser.parse_args()

        item = ItemModel.find_item_by_name(name)
        new_item = ItemModel(name, **req)

        if item is None:
            try:
                new_item.save_to_db()
                return {"message": "Item created"}, 201
            except:
                return {"message": "Item creation failed"}, 500
        return {"message": "Item already exists"}, 400

    @staticmethod
    def put(name):
        req = Item.parser.parse_args()

        item = ItemModel.find_item_by_name(name)

        if item is None:
            item = ItemModel(name, **req)
        else:
            item.price = req['price']
        item.save_to_db()
        return item.json()

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'You must be an admin to perform this action'}, 401
        item = ItemModel.find_item_by_name(name)
        if item:
            try:
                item.delete()
                return {"message": "Item Deleted"}, 201
            except:
                return {"message": "Error when deleting item"}, 400
        return {"message": "Item not found"}, 400




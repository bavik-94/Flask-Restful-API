from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel



class Items(Resource):
    @staticmethod
    def get():
        return ItemModel.get_all_items()


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
            return {"name": item.name, "price": item.price, "store_id": item.store_id}, 200
        return {"message": "Item not Found"}

    @staticmethod
    def post(name):
        req = Item.parser.parse_args()

        item = ItemModel.find_item_by_name(name)
        new_item = ItemModel(name, req['price'], req['store_id'])

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
            item = ItemModel(name, req['price'], req['store_id'])
        else:
            item.price = req['price']
        item.save_to_db()
        return item.json()


    @staticmethod
    def delete(name):
        item = ItemModel.find_item_by_name(name)
        if item:
            try:
                item.delete()
                return {"message": "Item Deleted"}, 201
            except:
                return {"message": "Error when deleting item"}, 400
        return {"message": "Item not found"}, 400




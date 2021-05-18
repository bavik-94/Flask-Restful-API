from db import db
from models.item import ItemModel


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic') # dynamic turns items into a query instead of a list

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name}

    @classmethod
    def get_all_stores(cls):
        return {'stores': list(x.json() for x in cls.query.all())}

    def get_all_items(self):
        return {'id': self.id, 'name': self.name, 'items': list(item.json() for item in self.items.all())}

    @classmethod
    def find_store_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name=name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

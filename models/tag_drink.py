from db import db

class TagDrinkModel(db.Model):

    __tablename__ = 'tag_drink'

    id = db.Column(db.Integer, primary_key=True)

    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    
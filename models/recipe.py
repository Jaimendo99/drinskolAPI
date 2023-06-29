from db import db

class RecipeModel(db.Model):

    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'), nullable=False)
    ingridient_id = db.Column(db.Integer, db.ForeignKey('ingridient.id'), nullable=False)
    quantity = db.Column(db.Float(precision=2), nullable=False)
    order = db.Column(db.Integer, nullable=False)

    drink = db.relationship('DrinkModel', back_populates='recipes')
    ingridient = db.relationship('IngridientModel', back_populates='recipes', )


  
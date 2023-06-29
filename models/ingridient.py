from db import db


class IngridientModel(db.Model):

    __tablename__ = 'ingridient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    alcohol_porcentage = db.Column(db.Float(precision=2), nullable=False)
    image_src = db.Column(db.String(255), nullable=False)

    # drinks = db.relationship('DrinkModel',back_populates = 'ingridients' , secondary='recipe')
    recipes = db.relationship('RecipeModel', back_populates = 'ingridient')

     
    
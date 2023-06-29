from db import db

class DrinkModel(db.Model):

    __tablename__ = 'drink'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    alcohol_porcentage = db.Column(db.Float(precision=2), nullable=False)
    image_src = db.Column(db.String(255), nullable=False)

    # ingridients = db.relationship('IngridientModel', back_populates = 'drinks', secondary='recipe')
    tags = db.relationship('TagModel', back_populates = 'drinks', secondary='tag_drink')
    users = db.relationship('UserModel', back_populates = 'drinks', secondary='experience')
    recipes = db.relationship('RecipeModel', back_populates = 'drink')

    
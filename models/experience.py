from db import db

class ExperienceModel(db.Model):

    __tablename__ = 'experience'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'), nullable=False)

    rating = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.String(255), nullable=True)
    wishlist = db.Column(db.Boolean, nullable=True)
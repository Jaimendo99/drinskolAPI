from db import db
from passlib.hash import pbkdf2_sha256 as sha256

class UserModel(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    image_src = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    drinks = db.relationship('DrinkModel', back_populates = 'users', secondary='experience')


    def check_password(self, password):
        try:
            ver = sha256.verify(password, self.password)
        except ValueError:
            ver = password == self.password
        return ver
from db  import db

class TagModel(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    
    drinks = db.relationship('DrinkModel', back_populates='tags', secondary='tag_drink')
    
        
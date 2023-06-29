from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from resources.utils import admin_required

from db import db
from models import TagDrinkModel
from schema import TagDrinkSchema, CreateTagDrinkSchema

tag_drink_blp = Blueprint(
    'tag_drink',
    __name__,
    url_prefix='/api/tag_drink',
    description='Operations on tag_drink'
)


@tag_drink_blp.route('/')
class TagDrink(MethodView):

    @tag_drink_blp.response(200, TagDrinkSchema(many=True))
    def get(self):
        """Get all tag_drinks"""
        tag_drinks = TagDrinkModel.query.all()
        return tag_drinks
        

    @jwt_required()
    @admin_required
    @tag_drink_blp.arguments(CreateTagDrinkSchema)
    @tag_drink_blp.response(201, TagDrinkSchema)
    def post(self, new_data):
        """Create new tag_drink"""
        tag_drink = TagDrinkModel(**new_data)
        try:    
            db.session.add(tag_drink)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e.__dict__['orig']))
        return tag_drink


@tag_drink_blp.route('/<int:id>')
class TagDrinkById(MethodView):
        
        @jwt_required()
        @admin_required
        @tag_drink_blp.response(204)
        def delete(self, id):
            """Delete tag_drink by id"""
            tag_drink = TagDrinkModel.query.get_or_404(id)
            try:
                db.session.delete(tag_drink)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(400, message=str(e.__dict__['orig']))
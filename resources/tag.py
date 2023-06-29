from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from resources.utils import admin_required

from db import db
from models import TagModel
from schema import TagSchema, BaseTagSchema

tag_blp = Blueprint(
    'tag',
    __name__,
    url_prefix='/api/tag',
    description='Operations on tag'
)


@tag_blp.route('/')
class Tag(MethodView):
    
    @tag_blp.response(200, BaseTagSchema(many=True))
    def get(self):
        """Get all tags"""
        tags = TagModel.query.all()
        return tags
        
    @jwt_required()
    @admin_required
    @tag_blp.arguments(BaseTagSchema)
    @tag_blp.response(201, BaseTagSchema)
    def post(self, new_data):
        """Create new tag"""
        tag = TagModel(**new_data)
        try:    
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e.__dict__['orig']))
        return tag
        
    

@tag_blp.route('/<int:id>')
class TagById(MethodView):
         
    @tag_blp.response(200, TagSchema)
    def get(self, id):
        """Get tag by id"""
        tag = TagModel.query.get_or_404(id)
        return tag

    @jwt_required()
    @admin_required
    @tag_blp.response(204)
    def delete(self, id):
        """Delete tag by id"""
        tag = TagModel.query.get_or_404(id)
        try:
            db.session.delete(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e.__dict__['orig']))
        return '', 204




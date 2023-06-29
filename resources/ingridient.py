from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError
from resources.utils import admin_required

from db import db
from models import IngridientModel
from schema import BaseIngridientSchema, IngridientSchema

ingridient_blp = Blueprint(
    'ingridient',
    __name__,
    url_prefix='/api/ingridient',
    description='Operations on ingridient'
)


@ingridient_blp.route('/')
class Ingridient(MethodView):

    @ingridient_blp.response(200, BaseIngridientSchema(many=True))
    def get(self):
        """Get all ingridients"""
        ingridients = IngridientModel.query.all()
        return ingridients
        
    @jwt_required()
    @admin_required
    @ingridient_blp.arguments(BaseIngridientSchema)
    @ingridient_blp.response(201, BaseIngridientSchema)
    def post(self, new_data):
        """Create new ingridient"""
        ingridient = IngridientModel(**new_data)
        try:    
            db.session.add(ingridient)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e.__dict__['orig']))
        return ingridient
    


@ingridient_blp.route('/<int:id>')
class IngridientById(MethodView):

    @ingridient_blp.response(200, IngridientSchema)
    def get(self, id):
        """Get ingridient by id"""
        ingridient = IngridientModel.query.get_or_404(id)
        return ingridient
    
    @jwt_required(fresh=True)
    @admin_required
    @ingridient_blp.arguments(BaseIngridientSchema)
    @ingridient_blp.response(200, BaseIngridientSchema)
    def put(self, new_data, id):
        """Update ingridient by id"""
        ingridient = IngridientModel.query.get_or_404(id)
        for key, value in new_data.items():
            setattr(ingridient, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e.__dict__['orig']))
        return ingridient


    @jwt_required(fresh=True)
    @admin_required
    @ingridient_blp.response(204)
    def delete(self, id):
        """Delete ingridient by id"""
        ingridient = IngridientModel.query.get_or_404(id)
        try:
            db.session.delete(ingridient)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e.__dict__['orig']))
        return {"message": f"Ingridient {id} deleted"}
    
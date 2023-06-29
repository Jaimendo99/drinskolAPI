from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import DrinkModel, RecipeModel,ExperienceModel, UserModel
from schema import BaseDrinkSchema, GetDrinkSchema

from resources.utils import admin_required

drink_blp = Blueprint(
    'drink',
    __name__,
    url_prefix='/api/drink',
    description='Operations on drink'
)


@drink_blp.route('/')
class Drink(MethodView):

    @drink_blp.response(200, BaseDrinkSchema(many=True))
    def get(self):
        """Get all drinks"""
        drinks = DrinkModel.query.all()
        return drinks
        

    @jwt_required()
    @admin_required
    @drink_blp.arguments(BaseDrinkSchema)
    @drink_blp.response(201, BaseDrinkSchema)
    def post(self, new_data):

        identity = get_jwt_identity()
        user = UserModel.query.get(identity)
        if not user.is_admin:
            abort(401, message="Admin privilege required")

        """Create new drink"""
        drink = DrinkModel(**new_data)
        try:    
            db.session.add(drink)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e.__dict__['orig']))
        return drink
    

@drink_blp.route('/<int:id>')
class DrinkById(MethodView):

    @drink_blp.response(200, GetDrinkSchema)
    def get(self, id):
        """Get drink by id"""
        drink = DrinkModel.query.get_or_404(id)
        return drink

    @jwt_required(fresh=True)
    @admin_required
    @drink_blp.arguments(BaseDrinkSchema)
    @drink_blp.response(200, BaseDrinkSchema)
    def put(self, new_data, id):

        identity = get_jwt_identity()
        user = UserModel.query.get(identity)
        if not user.is_admin:
            abort(401, message="Admin privilege required")

        """Update drink by id"""
        drink = DrinkModel.query.get_or_404(id)
        for key, value in new_data.items():
            setattr(drink, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e.__dict__['orig']))
        return drink

    
    @jwt_required(fresh=True)
    @admin_required
    # @drink_blp.response(204)
    def delete(self, id):
        """Delete drink by id"""
        drink = DrinkModel.query.get_or_404(id)
        recipe = RecipeModel.query.filter_by(drink_id=id)
        experience = ExperienceModel.query.filter_by(drink_id=id)

        recipes_id, experiences_id = [], []
        try:
            for r in recipe:
                recipes_id.append(r.id)
                db.session.delete(r)
            for e in experience:
                experiences_id.append(e.id)
                db.session.delete(e)
            db.session.delete(drink)
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e.__dict__['orig']))
        return {"message":f'Recipes {recipes_id} and experiences {experiences_id} were also deleted', "code": 204}
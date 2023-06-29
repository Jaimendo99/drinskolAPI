from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from resources.utils import admin_required
from db import db
from models import RecipeModel
from schema import BaseRecipeSchema, CreateRecipeEntrySchema, RecipeSchema

recipe_blp = Blueprint(
    'recipe',
    __name__,
    url_prefix='/api/recipe',
    description='Operations on recipe'
)


@recipe_blp.route('/')
class Recipe(MethodView):
        
        @recipe_blp.response(200, RecipeSchema(many=True))
        def get(self):
            """Get all recipes"""
            recipes = RecipeModel.query.all()
            return recipes
        
        @jwt_required()
        @admin_required
        @recipe_blp.arguments(CreateRecipeEntrySchema)
        @recipe_blp.response(201, RecipeSchema)
        def post(self, new_data):
            """Create new recipe"""
            recipe = RecipeModel(**new_data)
            try:    
                db.session.add(recipe)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(400, message=str(e.__dict__['orig']))
            return recipe
        

@recipe_blp.route('/<int:id>')
class RecipeById(MethodView):
    
        @recipe_blp.response(200, RecipeSchema)
        def get(self, id):
            """Get recipe by id"""
            recipe = RecipeModel.query.get_or_404(id)
            return recipe



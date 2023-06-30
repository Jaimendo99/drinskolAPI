import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import sql_conn_str, jwt_secret_key


from db import db
from blocklist import BLOCKLIST

from resources.user import user_blp as UserBlueprint
from resources.ingridient import ingridient_blp as IngridientBlueprint
from resources.drink import drink_blp as DrinkBlueprint
from resources.tag import tag_blp as TagBlueprint
from resources.experience import experience_blp as ExperienceBlueprint
from resources.recipe import recipe_blp as RecipeBlueprint
from resources.tag_drink import tag_drink_blp as TagDrinkBlueprint
from resources.fb_images import image_blp as ImageBlueprint


def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = sql_conn_str
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    api = Api(app)
    migrate = Migrate(app, db)


    app.config["JWT_SECRET_KEY"] = jwt_secret_key  

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({"description": "The token has been revoked", "error": "token_revoked"}), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({"description": "The token is not fresh", "error": "fresh_token_required"}), 401
    

    with app.app_context():
        db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(IngridientBlueprint)
    api.register_blueprint(DrinkBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(ExperienceBlueprint)
    api.register_blueprint(RecipeBlueprint)
    api.register_blueprint(TagDrinkBlueprint)
    api.register_blueprint(ImageBlueprint)
    

    return app



if __name__ == "__main__":
    app = create_app()
    app.run(debug=False)


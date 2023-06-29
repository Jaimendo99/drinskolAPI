from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (create_access_token, jwt_required, get_jwt_identity, get_jwt,
                                create_refresh_token )
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256 as sha256
from resources.utils import admin_required

from db import db
from blocklist import BLOCKLIST
from models import UserModel
from schema import BaseUserSchema, UserSchema, UserLoginSchema

user_blp = Blueprint(
    'user',
    __name__,
    url_prefix='/api/user',
    description='Operations on user'
)


@user_blp.route('/login')
class UserLogin(MethodView):

    @user_blp.arguments(UserLoginSchema)
    def post(self, login_data):
        """Login user"""
        user = UserModel.query.filter_by(username=login_data['username']).first()
        if user and user.check_password(login_data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}
        else:
            abort(401, message="Invalid username or password")


@user_blp.route('/refresh')
class UserRefresh(MethodView):
    
        @jwt_required(refresh=True)
        def post(self):
            """Refresh user token"""
            identity = get_jwt_identity()
            access_token = create_access_token(identity=identity, fresh=False)
            return {'access_token': access_token}


@user_blp.route('/logout')
class UserLogout(MethodView):
    
        @jwt_required()
        def post(self):
            jti = get_jwt()['jti']
            BLOCKLIST.add(jti)
            return {'message': 'Logged out'}, 200
        

@user_blp.route('/')
class User(MethodView):

    @user_blp.response(200, BaseUserSchema(many=True))
    @jwt_required()
    @admin_required
    def get(self):
        """Get all users"""
        users = UserModel.query.all()
        return users

    @jwt_required(optional=True)
    @user_blp.arguments(BaseUserSchema)
    @user_blp.response(201, BaseUserSchema)
    def post(self, new_data):
        """Create new user"""
        new_user = UserModel(**new_data)

        identity = get_jwt_identity()
        if identity:
            log_user = UserModel.query.get(identity)
            if new_user['is_admin'] and not log_user.is_admin:
                abort(401, message="Admin privilege required")
        else:
            new_user.is_admin = False

        # check if user exists
        if UserModel.query.filter_by(username=new_user.username).first():
            abort(400, message="User with that username already exists")
        if UserModel.query.filter_by(email=new_user.email).first():
            abort(400, message="User with that email already exists")
        # hash password
        new_user.password = sha256.hash(new_user.password)

        try:    
            db.session.add(new_user)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e.__dict__['orig']))
        return new_user
    

@user_blp.route('/<int:id>')
class UserById(MethodView):

    @jwt_required()
    @user_blp.response(200, UserSchema)
    def get(self, id):

        log_id = get_jwt_identity()
        log_user = UserModel.query.get(log_id)
        if not log_user.is_admin:
            if log_id != id:
                abort(401, message="Unauthorized")

        """Get user by id"""

        user = UserModel.query.get_or_404(id)
        return user


    @jwt_required(fresh=True)
    @user_blp.arguments(BaseUserSchema)
    @user_blp.response(200, BaseUserSchema)
    def put(self, new_data, id):

        log_id = get_jwt_identity()
        log_user = UserModel.query.get(log_id)
        if not log_user.is_admin:
            if log_id != id:
                abort(401, message="Unauthorized")

        """Update user by id"""
        user = UserModel.query.get_or_404(id)
        if user:
            for key, value in new_data.items():
                setattr(user, key, value)
        else:
            user = UserModel(id=id , **new_data)
        db.session.add(user)
        db.session.commit()
        return user


    @jwt_required(fresh=True)
    @admin_required
    @user_blp.response(204)
    def delete(self, id):
        """Delete user by id"""
    
        user = UserModel.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "User deleted successfully"}, 204


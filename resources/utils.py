from flask_smorest import abort
from flask_jwt_extended import  get_jwt_identity
from models import UserModel
from functools import wraps


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        user = UserModel.query.get(identity)
        if not user.is_admin:
            abort(401, message="Admin privilege required")
        return f(*args, **kwargs)
    return wrapper
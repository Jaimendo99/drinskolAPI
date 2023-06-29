from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ExperienceModel, UserModel
from schema import ExperienceSchema, BaseExperienceSchema

experience_blp = Blueprint(
    'experience',
    __name__,
    url_prefix='/api/experience',
    description='Operations on experience'
)


@experience_blp.route('/')
class Experience(MethodView):
    
        @experience_blp.response(200, ExperienceSchema(many=True))
        def get(self):
            """Get all experiences"""
            experiences = ExperienceModel.query.all()
            return experiences
            
    
        @experience_blp.arguments(ExperienceSchema)
        @experience_blp.response(201, ExperienceSchema)
        def post(self, new_data):
            """Create new experience"""
            experience = ExperienceModel(**new_data)
            try:    
                db.session.add(experience)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                abort(400, message=str(e.__dict__['orig']))
            return experience


@experience_blp.route('/<int:id>')
class ExperienceById(MethodView):
            
    @jwt_required()
    @experience_blp.response(200, ExperienceSchema)
    def get(self, id):
        experience = ExperienceModel.query.get_or_404(id)

        log_user_id = get_jwt_identity()
        log_user = UserModel.query.get_or_404(log_user_id)
        if not log_user.is_admin:
            if experience.user_id != log_user_id:
                abort(403, message='You are not allowed to see this experience')
        return experience

    @jwt_required()
    @experience_blp.arguments(BaseExperienceSchema)
    @experience_blp.response(200, ExperienceSchema)
    def put(self, new_data, id):
        """Update experience by id"""        

        user_id = get_jwt_identity()
        rating = new_data.get('rating')
                        
        if rating and (rating < 0 or rating > 5):
            abort(400, message='Rating must be between 0 and 5') 

        experience = ExperienceModel.query.get_or_404(id)

        experience['user_id'] = user_id

        for key, value in new_data.items():
            setattr(experience, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, message=str(e.__dict__['orig']))
        return experience
    

@experience_blp.route('/drink/<int:drink_id>')
class ExperienceByDrinkId(MethodView):
    
    @experience_blp.response(200, ExperienceSchema(many=True))
    def get(self, drink_id):
        """Get experience by drink id"""
        experiences = ExperienceModel.query.filter_by(drink_id=drink_id).all()

        rating_avg = 0
        comments = []
        whishlist_count = 0

        for experience in experiences:
            rating_avg += experience.rating
            if experience.comment:
                comments.append(experience.comment)
            if experience.whishlist:
                whishlist_count += 1
        if len(experiences) > 0:
            rating_avg = rating_avg / len(experiences)
        return {'rating_avg': rating_avg, 'comments': comments, 'whishlist_count': whishlist_count}

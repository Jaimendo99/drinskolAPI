import pyrebase
from resources.config import Config

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import UploadImageSchema
import base64
# serializers



image_blp = Blueprint(
    'image',
    __name__,
    url_prefix='/api/image',
    description='images operations'
)

firebase = pyrebase.initialize_app(Config)
storage = firebase.storage()

@image_blp.route('/')
class Image(MethodView):
    
    @image_blp.arguments(UploadImageSchema)
    @image_blp.response(201)
    def post(self, new_data):
        class_name = new_data['class_name']
        class_id = new_data['class_id']
        image_extension = new_data['image_extension']

        if image_extension == 'svg':
            content_type = 'image/svg+xml'
        else:
            content_type = f'image/{image_extension}'

        file_name = f'{class_name}_{class_id}.{image_extension}'
        img64 = new_data['image']
        
        storage.bucket.blob(file_name).upload_from_string(base64.b64decode(img64), content_type=content_type)

        img_url = f"https://firebasestorage.googleapis.com/v0/b/drinskolapi.appspot.com/o/{file_name}?alt=media"
        
        return {'message': 'image uploaded successfully','img_url': img_url}
    

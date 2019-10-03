from flask_restplus import reqparse
from werkzeug.datastructures import FileStorage

file_upload = reqparse.RequestParser()
file_upload.add_argument('image',
                         type=FileStorage,
                         location='files',
                         required=False,
                         help='Image file')
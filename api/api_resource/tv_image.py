from flask_restx import Resource, Namespace, fields
from utils import file_processor, database_processor, sql_processor
from flask_restx import reqparse, inputs
from flask import request
import werkzeug
from werkzeug.utils import secure_filename

api = Namespace('image', description='Operations on table image_table')

model_image_table = api.model('image_table', {
    'id': fields.Integer(required=True, description='The identifier'),
    'image_url': fields.String(required=True, description='Bildquelle'),
    'image_name': fields.String(required=True, description='Name des Bildes'),
})

updateParser = reqparse.RequestParser()
updateParser.add_argument('id', required=True, type=int)
updateParser.add_argument('column', required=True, type=str)
updateParser.add_argument('value', required=True, type=str)

insertParser = reqparse.RequestParser()
insertParser.add_argument('id', required=True, type=int)
insertParser.add_argument('image_url', required=True, type=str)
insertParser.add_argument('image_name', required=True, type=str)

deleteParser = reqparse.RequestParser()
deleteParser.add_argument('id', required=True, type=int)
class GetImageTableList(Resource):
    @api.marshal_with(model_image_table)
    def get(self):    
        QUERY_SELECT_IMAGE_TABLE= file_processor.read_sql_file(
            "sql/tv_image/select_tv_image.sql")
        sql_creation = QUERY_SELECT_IMAGE_TABLE
        
        ImageTableList = database_processor.fetch_data_in_database(sql_creation)
        print(ImageTableList)
        column = ['id','image_url','image_name']
        items = [dict(zip(column, row)) for row in ImageTableList]
        if items:
            return items
        api.abort(404)

    @api.doc(parser=updateParser)
    def put(self):
        args = updateParser.parse_args()
        QUERY_UPDATE_IMAGE_TABLE = file_processor.read_sql_file(
        "sql/tv_image/update_tv_image.sql")
        sql_creation = QUERY_UPDATE_IMAGE_TABLE.format(args['column'], "\'{}\'".format(args['value']),args['id'])

        database_processor.insert_data_into_database(sql_creation)
        return 201

    @api.doc(parser=insertParser)
    def post(self):
        args = insertParser.parse_args()
        QUERY_INSERT_IMAGE_TABLE = file_processor.read_sql_file(
        "sql/tv_image/insert_tv_image.sql")
        sql_creation = QUERY_INSERT_IMAGE_TABLE.format(args['id'], "\'{}\'".format(args['image_url']), "\'{}\'".format(args['image_name']))
        sql_creation = sql_processor.handleNone(sql_creation)
        database_processor.insert_data_into_database(sql_creation)
        return 201

    @api.doc(parser=deleteParser)
    def delete(self):
        args = deleteParser.parse_args()
        QUERY_DELETE_IMAGE_TABLE = file_processor.read_sql_file(
        "sql/tv_image/delete_tv_image.sql")
        sql_creation = QUERY_DELETE_IMAGE_TABLE.format(args['id'])

        database_processor.insert_data_into_database(sql_creation)
        return 201

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

uploadParser = reqparse.RequestParser()
uploadParser.add_argument('filename',location='files', type=werkzeug.datastructures.FileStorage, required=False)
class UploadImage(Resource):  
    @api.expect(uploadParser)
    def post(self):
        #pass
        args = uploadParser.parse_args()
        print(args)
        uploaded_file = args['filename']  # This is FileStorage instance
        print(uploaded_file)
        #filename = secure_filename(uploaded_file.filename)
        return ({'nextVal': args},201)




    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS    
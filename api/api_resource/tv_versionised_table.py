from flask_restx import Resource, Namespace, fields
from utils import file_processor, database_processor
from flask_restx import reqparse, inputs
from flask import request

api = Namespace('versionised_table', description='Operations on table versionised_table')

# model_versionised_table = api.model('versionised_table', {
#     'id': fields.Integer(required=True, description='The identifier'),
#     'normal_col': fields.String(required=True, description='New values in this column will lead to versioning in table'),
#     'update_col': fields.String(required=True, description='New values in this column will be updated in latest row'),
#     'ignore_col': fields.String(required=True, description='New values will be ignored, except when versioning takes place at the same time.'),
# })

model_versionised_table = api.model('versionised_table', {
    'nextVal': fields.Integer(required=True, description='The next identifier;'),
    'payload': fields.List(fields.Nested(api.model('ordinary_table_payload', {        
        'id': fields.Integer(required=True, description='The identifier'),
        'normal_col': fields.String(required=True, description='New values in this column will lead to versioning in table'),
        'update_col': fields.String(required=True, description='New values in this column will be updated in latest row'),
        'ignore_col': fields.String(required=True, description='New values will be ignored, except when versioning takes place at the same time.'),
    })))
})

post_model_versionised_table = api.model('versionised_table_post', {
    'nextVal': fields.Integer(required=True, description='The next identifier;')
})

updateParser = reqparse.RequestParser()
updateParser.add_argument('id', required=True, type=int)
updateParser.add_argument('column', required=True, type=str)
updateParser.add_argument('value', required=True, type=str)

insertParser = reqparse.RequestParser()
insertParser.add_argument('id', required=True, type=int)
insertParser.add_argument('normal_col', required=True, type=str)
insertParser.add_argument('update_col', required=True, type=str)
insertParser.add_argument('ignore_col', required=True, type=str)

deleteParser = reqparse.RequestParser()
deleteParser.add_argument('id', required=True, type=int)
class GetVersionisedTableList(Resource):
    @api.marshal_with(model_versionised_table)
    def get(self):    
        QUERY_SELECT_VERSIONISED_TABLE= file_processor.read_sql_file(
            "sql/tv_versionised_table/select_tv_versionised_table.sql")
        sql_creation = QUERY_SELECT_VERSIONISED_TABLE
       
        VersionisedTableList = database_processor.fetch_data_in_database(sql_creation)
        column = ['id','normal_col','update_col','ignore_col']
        items = [dict(zip(column, row)) for row in VersionisedTableList]
        # START Get nextVal
        QUERY_NEXTVAL_VERSIONISED_TABLE = file_processor.read_sql_file(
            "sql/tv_versionised_table/nextval_tv_versionised_table.sql")
        sql_creation = QUERY_NEXTVAL_VERSIONISED_TABLE
        nextVal = database_processor.fetch_data_in_database(sql_creation)
        # END - Get nextVal
        if items:
            return {'payload': items, 'nextVal': nextVal[0][0]}
        api.abort(404)

    @api.doc(parser=updateParser)
    def put(self):
        args = updateParser.parse_args()
        QUERY_UPDATE_VERSIONISED_TABLE = file_processor.read_sql_file(
        "sql/tv_versionised_table/update_tv_versionised_table.sql")
        sql_creation = QUERY_UPDATE_VERSIONISED_TABLE.format(args['column'], "\'{}\'".format(args['value']),args['id'])

        database_processor.insert_data_into_database(sql_creation)
        return 201

    @api.doc(parser=insertParser)
    @api.doc(responses={
        400: 'Validation Error'
    })
    @api.marshal_with(post_model_versionised_table, code=201, description='Object created')
    def post(self):
        args = insertParser.parse_args()
        QUERY_INSERT_VERSIONISED_TABLE = file_processor.read_sql_file(
        "sql/tv_versionised_table/insert_tv_versionised_table.sql")
        sql_creation = QUERY_INSERT_VERSIONISED_TABLE.format(args['id'], "\'{}\'".format(args['normal_col']), "\'{}\'".format(args['update_col']), "\'{}\'".format(args['ignore_col']))

        database_processor.insert_data_into_database(sql_creation)
         # START Get nextVal
        QUERY_NEXTVAL_VERSIONISED_TABLE = file_processor.read_sql_file(
            "sql/tv_versionised_table/nextval_tv_versionised_table.sql")
        sql_creation = QUERY_NEXTVAL_VERSIONISED_TABLE
        nextVal = database_processor.fetch_data_in_database(sql_creation)
        # END - Get nextVal
        return ({'nextVal': nextVal[0][0]},201)

    @api.doc(parser=deleteParser)
    def delete(self):
        args = deleteParser.parse_args()
        QUERY_DELETE_VERSIONISED_TABLE = file_processor.read_sql_file(
        "sql/tv_versionised_table/delete_tv_versionised_table.sql")
        sql_creation = QUERY_DELETE_VERSIONISED_TABLE.format(args['id'])

        database_processor.insert_data_into_database(sql_creation)
        return 201
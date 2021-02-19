from flask_restx import Resource, Namespace, fields
from utils import file_processor, database_processor, sql_processor
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
    'autofill': fields.Nested(api.model('ordinary_table_payload', {
        'id': fields.Integer(required=True, description='The identifier; no primary key!')
    })),
    'payload': fields.List(fields.Nested(api.model('ordinary_table_payload', {        
        'id': fields.Integer(required=True, description='The identifier'),
        'normal_col': fields.String(required=True, description='New values in this column will lead to versioning in table'),
        'update_col': fields.String(required=True, description='New values in this column will be updated in latest row'),
        'ignore_col': fields.String(required=True, description='New values will be ignored, except when versioning takes place at the same time.'),
    })))
})

post_model_versionised_table = api.model('versionised_table_post', {
    'autofill': fields.Nested(api.model('ordinary_table_payload', {
        'id': fields.Integer(required=True, description='The identifier; no primary key!')
    })),
})

updateCellParser = reqparse.RequestParser()
updateCellParser.add_argument('id', required=True, type=int)
updateCellParser.add_argument('column', required=True, type=str)
updateCellParser.add_argument('value', required=True, type=str)

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
        VersionisedTableList = database_processor.fetch_data_in_database_pd_dataframe(QUERY_SELECT_VERSIONISED_TABLE).to_dict(orient="records")
        
         # START - Get nextId
        QUERY_NEXTID_VERSIONISED_TABLE = file_processor.read_sql_file(
            "sql/tv_versionised_table/nextid_tv_versionised_table.sql")
        sql_creation = QUERY_NEXTID_VERSIONISED_TABLE
        nextId = database_processor.fetch_data_in_database(sql_creation)
        # END - Get nextId
        if VersionisedTableList:
            return {'payload': VersionisedTableList, 'autofill': {'id': nextId[0][0]}}
        api.abort(404)

class GetVersionisedTableItem(Resource):        
    @api.doc(parser=insertParser)
    def put(self):
        args = insertParser.parse_args()
        QUERY_UPDATE_VERSIONISED_TABLE = file_processor.read_sql_file(
        "sql/tv_versionised_table/update_tv_versionised_table.sql")
        sql_creation = QUERY_UPDATE_VERSIONISED_TABLE.format("\'{}\'".format(args['normal_col']), "\'{}\'".format(args['update_col']), "\'{}\'".format(args['ignore_col']),args['id'])

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
        sql_creation = sql_processor.handleNone(sql_creation)
        database_processor.insert_data_into_database(sql_creation)
        # START Get nextId
        QUERY_NEXTID_VERSIONISED_TABLE = file_processor.read_sql_file(
            "sql/tv_versionised_table/nextid_tv_versionised_table.sql")
        sql_creation = QUERY_NEXTID_VERSIONISED_TABLE
        nextId = database_processor.fetch_data_in_database(sql_creation)
        # END - Get nextId
        return ({'autofill': {'id': nextId[0][0]}},201)

    @api.doc(parser=deleteParser)
    def delete(self):
        args = deleteParser.parse_args()
        QUERY_DELETE_VERSIONISED_TABLE = file_processor.read_sql_file(
        "sql/tv_versionised_table/delete_tv_versionised_table.sql")
        sql_creation = QUERY_DELETE_VERSIONISED_TABLE.format(args['id'])

        database_processor.insert_data_into_database(sql_creation)
        return 201

class GetVersionisedTableCell(Resource):        
    @api.doc(parser=updateCellParser)
    def put(self):
        args = updateCellParser.parse_args()
        QUERY_UPDATE_VERSIONISED_TABLE = file_processor.read_sql_file(
        "sql/tv_versionised_table/update_cell_tv_versionised_table.sql")
        sql_creation = QUERY_UPDATE_VERSIONISED_TABLE.format(args['column'], "\'{}\'".format(args['value']),args['id'])

        database_processor.insert_data_into_database(sql_creation)
        return 201
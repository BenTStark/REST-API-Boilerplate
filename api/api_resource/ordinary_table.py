from flask_restx import Resource, Namespace, fields
from utils import file_processor, database_processor
from flask_restx import reqparse, inputs
from flask import request

api = Namespace('ordinary_table', description='Operations on table ordinary_table')

model_ordinary_table = api.model('ordinary_table', {
    'id': fields.Integer(required=True, description='The identifier; no primary key!'),
    'info': fields.String(required=True, description='Info field for various text')
})

@api.response(404, 'Entry not found')
class GetOrdinaryTableList(Resource):
    @api.marshal_with(model_ordinary_table)
    def get(self):          
        QUERY_SELECT_ORDINARY_TABLE = file_processor.read_sql_file(
            "sql/ordinary_table/select_ordinary_table.sql")
        ordinaryTableList = database_processor.fetch_data_in_database(QUERY_SELECT_ORDINARY_TABLE)
        column = ['id','info']
        items = [dict(zip(column, row)) for row in ordinaryTableList]
        if items:
            return items
        api.abort(404)

getParser = reqparse.RequestParser()
getParser.add_argument('id', required=True, type=int,
                    help="Id cannot be blank!")

postParser = reqparse.RequestParser()
postParser.add_argument('info', required=False, type=str)

updateParser = reqparse.RequestParser()
updateParser.add_argument('id', required=True, type=int,
                    help="Id cannot be blank!")
updateParser.add_argument('info', required=False, type=str)

class GetOrdinaryTableItem(Resource):
    @api.doc(parser=getParser)
    @api.marshal_with(model_ordinary_table)
    def get(self):       
        args = getParser.parse_args()       
        QUERY_SELECT_ORDINARY_TABLE_ITEM = file_processor.read_sql_file(
            "sql/ordinary_table/select_ordinary_table_item.sql")
        sql_creation = QUERY_SELECT_ORDINARY_TABLE_ITEM.format(args['id'])
        ordinaryTableListItem = database_processor.fetch_data_in_database(sql_creation)
        column = ['id','info']
        items = [dict(zip(column, row)) for row in ordinaryTableListItem]
        if items:
            return items
        api.abort(404)
    
    @api.doc(parser=postParser)
    def post(self):
        args = postParser.parse_args()    
        QUERY_INSERT_ORDINARY_TABLE_ITEM = file_processor.read_sql_file(
            "sql/ordinary_table/insert_ordinary_table_item.sql")
        sql_creation = QUERY_INSERT_ORDINARY_TABLE_ITEM.format("\'{}\'".format(args['info']))
        database_processor.insert_data_into_database(sql_creation)
        return 201

    @api.doc(parser=updateParser)
    def put(self):
        args = updateParser.parse_args()    
        QUERY_UPDATE_ORDINARY_TABLE_ITEM = file_processor.read_sql_file(
            "sql/ordinary_table/update_ordinary_table_item.sql")
        sql_creation = QUERY_UPDATE_ORDINARY_TABLE_ITEM.format("\'{}\'".format(args['info']), args['id'])
        database_processor.insert_data_into_database(sql_creation)
        return 201
    
    @api.doc(parser=getParser)
    def delete(self):
        args = getParser.parse_args()    
        QUERY_DELETE_ORDINARY_TABLE_ITEM = file_processor.read_sql_file(
            "sql/ordinary_table/delete_ordinary_table_item.sql")
        sql_creation = QUERY_DELETE_ORDINARY_TABLE_ITEM.format(args['id'])
        database_processor.insert_data_into_database(sql_creation)
        return 201

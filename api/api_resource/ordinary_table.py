from flask_restx import Resource, Namespace, fields
from utils import file_processor, database_processor, sql_processor
from flask_restx import reqparse, inputs
from flask import request

api = Namespace('ordinary_table',
                description='Operations on table ordinary_table')

# schema = {'nextVal': fields.Integer(required=True, description='The next identifier;')}
# schema['payload'] = {}
# schema['payload']['id'] = fields.Integer(required=True, description='The identifier; no primary key!')
# schema['payload']['info'] = fields.String(required=True, description='Info field for various text')

model_ordinary_table = api.model('ordinary_table', {
    'autofill': fields.Nested(api.model('ordinary_table_payload', {
        'id': fields.Integer(required=True, description='The identifier; no primary key!')
    })),
    'payload': fields.List(fields.Nested(api.model('ordinary_table_payload', {
        'id': fields.Integer(required=True, description='The identifier; no primary key!'),
        'info': fields.String(required=True, description='Info field for various text')
    })))
})

post_model_ordinary_table = api.model('ordinary_table_post', {
    'autofill': fields.Nested(api.model('ordinary_table_payload', {
        'id': fields.Integer(required=True, description='The identifier; no primary key!')
    }))
})


@api.response(404, 'Entry not found')
class GetOrdinaryTableList(Resource):
    @api.marshal_with(model_ordinary_table)
    def get(self):
        QUERY_SELECT_ORDINARY_TABLE = file_processor.read_sql_file(
            "sql/ordinary_table/select_ordinary_table.sql")
        ordinaryTableList = database_processor.fetch_data_in_database_pd_dataframe(
            QUERY_SELECT_ORDINARY_TABLE).to_dict(orient="records")
        # START - Get nextId
        QUERY_NEXTID_ORDINARY_TABLE = file_processor.read_sql_file(
            "sql/ordinary_table/nextid_ordinary_table.sql")
        sql_creation = QUERY_NEXTID_ORDINARY_TABLE
        nextId = database_processor.fetch_data_in_database(sql_creation)
        # END - Get nextId
        if ordinaryTableList:
            return {'payload': ordinaryTableList, 'autofill': {'id': nextId[0][0]}}
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
        ordinaryTableListItem = database_processor.fetch_data_in_database_pd_dataframe(
            sql_creation).to_dict(orient="records")
        # START - Get nextId
        QUERY_NEXTID_ORDINARY_TABLE = file_processor.read_sql_file(
            "sql/ordinary_table/nextid_ordinary_table.sql")
        sql_creation = QUERY_NEXTID_ORDINARY_TABLE
        nextId = database_processor.fetch_data_in_database(sql_creation)
        # END - Get nextId
        if ordinaryTableListItem:
            return {'payload': ordinaryTableListItem, 'autofill': {'id': nextId[0][0]}}
        api.abort(404)
 
    @api.doc(parser=postParser)
    @api.doc(responses={
        400: 'Validation Error'
    }) 
    @api.marshal_with(post_model_ordinary_table, code=201, description='Object created')
    def post(self):
        args = postParser.parse_args()
        QUERY_INSERT_ORDINARY_TABLE_ITEM = file_processor.read_sql_file(
            "sql/ordinary_table/insert_ordinary_table_item.sql")
        sql_creation = QUERY_INSERT_ORDINARY_TABLE_ITEM.format(
            "\'{}\'".format(args['info']))
        sql_creation = sql_processor.handleNone(sql_creation)
        database_processor.insert_data_into_database(sql_creation)
        # START Get nextId
        QUERY_NEXTID_ORDINARY_TABLE = file_processor.read_sql_file(
            "sql/ordinary_table/nextid_ordinary_table.sql")
        sql_creation = QUERY_NEXTID_ORDINARY_TABLE
        nextId = database_processor.fetch_data_in_database(sql_creation)
        # END - Get nextId
        return ({'autofill':{'id': nextId[0][0]}}, 201)

    @api.doc(parser=updateParser)
    def put(self):
        args = updateParser.parse_args()
        QUERY_UPDATE_ORDINARY_TABLE_ITEM = file_processor.read_sql_file(
            "sql/ordinary_table/update_ordinary_table_item.sql")
        sql_creation = QUERY_UPDATE_ORDINARY_TABLE_ITEM.format(
            "\'{}\'".format(args['info']), args['id'])
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

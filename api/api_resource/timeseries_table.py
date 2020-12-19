from flask_restx import Resource, Namespace, fields
from utils import file_processor, database_processor
from flask_restx import reqparse, inputs
from flask import request

api = Namespace('timeseries_table', description='Operations on table timeseries_table')

model_timeseries_table = api.model('timeseries_table', {
    'id': fields.Integer(required=True, description='The identifier'),
    'info': fields.String(required=True, description='Some info'),
    'valid_from': fields.DateTime(required=True, description='valid from'),
    'valid_to': fields.DateTime(required=True, description='valid to'),
    'modified_at': fields.DateTime(required=True, description='modified at'),
    'changed_by': fields.String(required=True, description='changed_by')
})

@api.response(404, 'Entry not found')
class GetTimeseriesTableListNow(Resource):
    @api.marshal_with(model_timeseries_table)
    def get(self):          
        QUERY_SELECT_TIMESERIES_TABLE_NOW = file_processor.read_sql_file(
            "sql/timeseries_table/select_timeseries_table_now.sql")
        TimeseriesTableList = database_processor.fetch_data_in_database(QUERY_SELECT_TIMESERIES_TABLE_NOW)
        column = ['id','info','valid_from','valid_to','modified_at','changed_by']
        items = [dict(zip(column, row)) for row in TimeseriesTableList]
        if items:
            return items
        api.abort(404)

getParser = reqparse.RequestParser()
getParser.add_argument('date', required=False, type=inputs.datetime_from_iso8601,
                    help="Date cannot be bank!")
class GetTimeseriesTableListDate(Resource):
    @api.doc(parser=getParser)
    @api.marshal_with(model_timeseries_table)
    def get(self):  
        args = getParser.parse_args()    
        if 'date' in args:  
            QUERY_SELECT_TIMESERIES_TABLE_DATE= file_processor.read_sql_file(
                "sql/timeseries_table/select_timeseries_table_date.sql")
            sql_creation = QUERY_SELECT_TIMESERIES_TABLE_DATE.format("\'{}\'".format(args['date']))
        else:
            QUERY_SELECT_TIMESERIES_TABLE_NOW = file_processor.read_sql_file(
            "sql/timeseries_table/select_timeseries_table_now.sql") 
            sql_creation = QUERY_SELECT_TIMESERIES_TABLE_NOW
        
        TimeseriesTableList = database_processor.fetch_data_in_database(sql_creation)
        column = ['id','info','valid_from','valid_to','modified_at','changed_by']
        items = [dict(zip(column, row)) for row in TimeseriesTableList]
        if items:
            return items
        api.abort(404)

postParser = reqparse.RequestParser()
postParser.add_argument('id', required=True, type=int)
postParser.add_argument('info', required=True, type=str)
postParser.add_argument('valid_from', required=True, type=inputs.datetime_from_iso8601)
postParser.add_argument('valid_to', required=True, type=inputs.datetime_from_iso8601)
postParser.add_argument('changed_by', required=True, type=str)


deleteParser = reqparse.RequestParser()
deleteParser.add_argument('id', required=True, type=int)
deleteParser.add_argument('valid_to', required=True, type=inputs.datetime_from_iso8601)
class GetTimeseriesTableItem(Resource):  
    @api.doc(parser=postParser)
    def post(self):
        args = postParser.parse_args()
        QUERY_INSERT_TIMESERIES_TABLE_ITEM = file_processor.read_sql_file(
        "sql/timeseries_table/insert_timeseries_table_item.sql")
        sql_creation = QUERY_INSERT_TIMESERIES_TABLE_ITEM.format(args['id'], "\'{}\'".format(args['info']), "\'{}\'".format(args['valid_from']), "\'{}\'".format(args['valid_to']),"\'{}\'".format(args['changed_by']))

        database_processor.insert_data_into_database(sql_creation)
        return 201

    
    def put(self):
        pass

    @api.doc(parser=deleteParser)
    def delete(self):
        args = deleteParser.parse_args()
        QUERY_DELETE_TIMESERIES_TABLE_ITEM = file_processor.read_sql_file(
        "sql/timeseries_table/delete_timeseries_table_item.sql")
        sql_creation = QUERY_DELETE_TIMESERIES_TABLE_ITEM.format(args['id'], "\'{}\'".format(args['valid_to']))

        database_processor.insert_data_into_database(sql_creation)
        return 201
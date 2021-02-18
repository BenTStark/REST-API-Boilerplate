from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
from flask_restx import Resource, Api
import json
import yaml
import os
import psycopg2
from utils import file_processor, database_processor
import urllib.request
from api_resource import ordinary_table, timeseries_table, tv_versionised_table, tv_image


app = Flask(__name__)
CORS(app)
basic_api = Api(app,
    title='REST API Setup',
    version='1.0',
    description='A Simple setup for a Flask REST API')
#print(basic_api.namespace)

ordinary_table_api = ordinary_table.api
basic_api.add_namespace(ordinary_table_api,path='/ordinary')
ordinary_table_api.add_resource(ordinary_table.GetOrdinaryTableItem, '')
ordinary_table_api.add_resource(ordinary_table.GetOrdinaryTableList, '/list')

timeseries_table_api = timeseries_table.api
basic_api.add_namespace(timeseries_table_api,path='/timeseries')
timeseries_table_api.add_resource(timeseries_table.GetTimeseriesTableListDate ,'')
timeseries_table_api.add_resource(timeseries_table.GetTimeseriesTableItem, '/item')

tv_versionised_table_api = tv_versionised_table.api
basic_api.add_namespace(tv_versionised_table_api,path='/versionised')
tv_versionised_table_api.add_resource(tv_versionised_table.GetVersionisedTableItem, '')
tv_versionised_table_api.add_resource(tv_versionised_table.GetVersionisedTableList, '/list')

tv_image_api = tv_image.api
basic_api.add_namespace(tv_image_api,path='/image')
tv_image_api.add_resource(tv_image.GetImageTableList, '')
tv_image_api.add_resource(tv_image.UploadImage, '/upload', endpoint='with-parser')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

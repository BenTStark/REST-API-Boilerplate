import psycopg2
import yaml
import os.path 
import pandas as pd

with open(os.path.dirname(__file__) + '/../../config.yaml') as file:
    credentials = yaml.load(file,Loader=yaml.FullLoader)

connection = psycopg2.connect(host="localhost",database=credentials["database"]["database"], user=credentials["database"]["username"], password=credentials["database"]["password"])
def fetch_data_in_database(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def fetch_data_in_database_pd_dataframe(sql):
    data = pd.read_sql(sql, connection)
    print(data.shape)
    return data

def insert_data_into_database(sql):    
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    cursor.close()
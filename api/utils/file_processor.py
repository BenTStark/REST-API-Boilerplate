import os


def read_sql_file(input_file):
    sql_statement = ""
    api_path = str(os.getcwd())
    print('WORKING DIR')
    print(api_path)

    if "api" not in api_path:
        api_path = api_path + "/api"

    with open(api_path + "/" + input_file, 'r') as file:
        sql_statement = file.read().replace('\n', ' ')

    return sql_statement

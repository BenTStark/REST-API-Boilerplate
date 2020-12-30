import os

def handleNone(sql):
    sql = sql.replace(chr(39) + 'None' + chr(39),'NULL')
    sql = sql.replace('None','NULL')
    return sql

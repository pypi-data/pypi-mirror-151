import pandas as pd
import pymysql
from pymysql.cursors import DictCursor

connection_dict = {}
current_conn = None


def connect(host, port, user, passwd, db, conn_name=None):
    global current_conn
    conn = pymysql.connect(user=user, passwd=passwd, host=host, port=port, db=db)
    if conn_name is not None:
        connection_dict[conn_name] = conn
    current_conn = conn
    return conn


def close(conn):
    conn.close()


def query_data(sql, conn_name=None):
    conn = None
    if conn_name is not None:
        conn = connection_dict[conn_name]
    elif current_conn is not None:
        conn = current_conn
    if conn is None:
        raise Exception('database was not connected')
    cursor = conn.cursor(DictCursor)
    cursor.execute(sql)
    results = cursor.fetchall()
    df = pd.DataFrame(results)
    return df

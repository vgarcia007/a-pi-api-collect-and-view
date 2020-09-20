import os
import json
import time
import sqlite3
from sqlite3 import Error
import requests

script_dir = os.path.dirname(os.path.realpath('__file__'))
db_file = script_dir + '/common/database.db'

def get_api(ip, route='/', port='8000'):
    """ get data from api
    :param ip: id address 
    :param route: api route 
    :param port: host port
    :return: Connection object or False
    """
    try:
        response = requests.get('http://' + ip + ':' + port + route)
    except requests.ConnectionError as e:
        #print(e)
        return False
    
    if response.status_code == 200:
        return response.json()
    else:
        return False

def get_and_save_value_from_api(conn, hostname, ip, name, key, route='/', port='8000'):
    """ get a value from api and save 2 db
    :param conn: db connection
    :param ip: id address
    :param name: value for name field in db 
    :param route: api route 
    :param port: host port
    :return: Connection object or False
    """
    info = get_api(ip, route, port)
    if info == False:
        return False

    sensor_data = (
        hostname,
        name,
        info[key],
        time.time()
        )
    try:
        new_row = create_record(conn, sensor_data)
        print('OK: row for ' + name + ' inserted id:' + str(new_row))
    except:
        print('Fail: row for ' + name)
    
    


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_record(conn, record):
    """
    Create a new record into the records table
    :param conn:
    :param record:
    :return: record id
    """
    sql = ''' INSERT INTO records(hostname,name,data,recorded)
              VALUES(?,?,?,?) '''
    c = conn.cursor()
    c.execute(sql, record)
    conn.commit()
    return c.lastrowid
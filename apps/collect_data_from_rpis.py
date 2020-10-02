import os
import sqlite3
from sqlite3 import Error
from common.devices import devices
from common.functions import *

if __name__ == '__main__':

    script_dir = os.path.dirname(os.path.realpath('__file__'))
    db_file = script_dir + '/common/database.db'

    sql_create_records_table = """CREATE TABLE IF NOT EXISTS records (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        hostname text NOT NULL,
                                        name text NOT NULL,
                                        data text,
                                        recorded timestamp
                                    ); """

    # create a database connection
    conn = create_connection(db_file)

    # create tables
    if conn is not None:
        # create records table
        create_table(conn, sql_create_records_table)

    else:
        print("Error! cannot create the database connection.")
        quit()

    while True:
        for device in devices:

            print('Try: ' + device['ip'])
            info = get_api(device['ip'])
            if info == False:
                print('Fail: ' + device['ip'])
                continue

            #cpu temp
            get_and_save_value_from_api(conn, info['hostname'], device['ip'], 'cpu_temp', 'temp', '/cpu')
            #free ram
            get_and_save_value_from_api(conn, info['hostname'], device['ip'], 'memory_free', 'free', '/memory')
            #free disk space
            get_and_save_value_from_api(conn, info['hostname'], device['ip'], 'disk_free', 'free', '/disk')

            if 'one_wire' not in info:
                print('no 1-wire sensors attached')
            else:
                if 'ds1820' in info['one_wire']:

                    ds1820 = info['one_wire']['ds1820']
                    print(str(len(ds1820)) + ' ds1820 sensors attached')

                    for item in ds1820:
                        get_and_save_value_from_api(
                            conn,
                            info['hostname'],
                            device['ip'],
                            'ds1820' + item,
                            'temp_c',
                            '/one-wire/ds1820/' + item
                            )

            if 'serial' not in info:
                print('no serial sensors attached')
            else:
                if 'wde1' in info['serial']:

                    serial_wde1 = info['serial']['wde1']
                    print(str(len(serial_wde1)) + ' serial_wde1 sensors attached')

                    for item in serial_wde1:
                        get_and_save_value_from_api(
                            conn,
                            info['hostname'],
                            device['ip'],
                            'wde1-' + item,
                            item,
                            '/serial/wde1/' + item
                            )

        time.sleep(1800)
        
import sqlite3
from sqlite3 import Error
from common.devices import devices
from common.functions import get_api, get_and_save_value_from_api, create_connection, script_dir, db_file
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from dateutil import tz


app = Flask(__name__, static_folder="static_files")

@app.route('/')
def home():

    api_data=[]

    i=0
    for device in devices:

        
        info = get_api(device['ip'])
        if info == False:
            print('Fail: ' + device['ip'])
            continue
        info['device']=device
        api_data.append(info)
        i=i+1

    return render_template('home.html', api_data=api_data)


@app.route('/db_test')
def db_test():
    conn = create_connection(db_file)
    c = conn.cursor()
    sql = ''' SELECT * FROM records'''
    c.execute(sql)
    db_data = c.fetchall()

    return render_template('db_test.html', data=db_data)

@app.route('/pi/<pi>')
def pi(pi):
    pi_ip = ''
    db_data = []
    conn = create_connection(db_file)


    for device in devices:
        if device['name'] == pi:
            
            device_name= pi

            latest_data = {}
            pi_ip = device['ip']

            info = get_api(device['ip'])
            c = conn.cursor()
            sql = ''' SELECT data, recorded FROM records WHERE hostname = ? AND name = "cpu_temp" ORDER BY recorded DESC  LIMIT 1'''
            c.execute(sql, (info['hostname'],))
            latest_data['cpu_temp'] = c.fetchall()[0]

            db_data.append(latest_data)

            sql = ''' SELECT data, recorded FROM records WHERE hostname = ? AND name = "memory_free" ORDER BY recorded DESC  LIMIT 1'''
            c.execute(sql, (info['hostname'],))
            latest_data['memory_free'] = c.fetchall()[0]

            db_data.append(latest_data)

            sql = ''' SELECT data, recorded FROM records WHERE hostname = ? AND name = "disk_free" ORDER BY recorded DESC  LIMIT 1'''
            c.execute(sql, (info['hostname'],))
            latest_data['disk_free'] = c.fetchall()[0]

            db_data.append(latest_data)

            if 'one_wire' in info:
                if 'ds1820' in info['one_wire']:
                    latest_data['ds1820'] = []

                    for item in info['one_wire']['ds1820']:
                        name = 'ds1820' + item
                        item_data = {}
                        item_data['name'] = name
                        print(name)
                        sql = ''' SELECT data, recorded FROM records WHERE hostname = ? AND name = ? ORDER BY recorded DESC  LIMIT 1'''
                        c.execute(sql, (info['hostname'],name,))
                        item_db = c.fetchall()[0]
                        item_data['temp'] = item_db[0]
                        item_data['recorded'] = item_db[1]
                        latest_data['ds1820'].append(item_data)

                        db_data.append(latest_data)

            if 'serial' in info:
                if 'wde1' in info['serial']:
                    latest_data['wde1'] = []

                    for item in info['serial']['wde1']:
                        name = 'wde1-' + item
                        item_data = {}
                        item_data['name'] = name
                        print(name)
                        sql = ''' SELECT data, recorded FROM records WHERE hostname = ? AND name = ? ORDER BY recorded DESC  LIMIT 1'''
                        c.execute(sql, (info['hostname'],name,))
                        item_db = c.fetchall()[0]
                        item_data['name'] = name
                        item_data['value'] = item_db[0]
                        item_data['recorded'] = item_db[1]
                        latest_data['wde1'].append(item_data)

                        db_data.append(latest_data)

    if len(pi_ip) == 0:
        return render_template('error.html', text='device not in list')

    return render_template('pi.html', device_name=device_name ,data=latest_data)


@app.route('/chart/<pi>/<sensor>')
def chart(pi, sensor):

    conn = create_connection(db_file)

    for device in devices:
        if device['name'] == pi:
            
            device_name= pi

            sensor_name = sensor

    return render_template('chart.html', device_name=device_name,pi=pi,sensor_name=sensor_name)

@app.route('/chart/json/<pi>/<sensor>')
def chart_json(pi, sensor):

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    conn = create_connection(db_file)
    conn.row_factory = sqlite3.Row

    json = []

    for device in devices:
        if device['name'] == pi:
            
            sensor_name = sensor

            info = get_api(device['ip'])

            c = conn.cursor()
            sql = ''' SELECT data, recorded FROM records WHERE hostname = ? AND name = ? ORDER BY recorded ASC'''
            c.execute(sql, (info['hostname'], sensor_name))
            db_data = c.fetchall()

            
            for data in db_data:

                timestamp = datetime.utcfromtimestamp(data[1])
                timestamp = timestamp.replace(tzinfo=from_zone)
                timestamp = timestamp.astimezone(to_zone)
                item = {
                    'value': float(data[0]),
                    'key':timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    }

                json.append(item)
                


    return jsonify(json)

if __name__ == '__main__':

    app.run(host='0.0.0.0')

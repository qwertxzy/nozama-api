from flask import Blueprint, request
from flask_api import status
import mysql.connector
import json
import conf

add_manufacturer = Blueprint('add_manufacturer', __name__)

@add_manufacturer.route('/add_manufacturer', methods=['POST'])
def handle():
    connector = mysql.connector.connect(
        user=conf.user,
        database=conf.database,
        passwd=conf.passwd,
        host=conf.host,
        port=conf.port)

    cursor = connector.cursor()

    data = request.get_json()

    manufacturer_name = data['manufacturer_name']
    manufacturer_description = data['manufacturer_description']

    return_status = cursor.callproc('add_manufacturer', args=[manufacturer_name, manufacturer_description, 0])

    answer = {}
    answer['manufacturer_id'] = return_status[2]

    connector.close()
    return json.dumps(answer), status.HTTP_200_OK
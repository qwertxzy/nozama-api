from flask import Blueprint
from flask_api import status
import mysql.connector
import json
import conf

manufacturers = Blueprint('manufacturers', __name__)

@manufacturers.route('/manufacturers')
def handle():
    connector = mysql.connector.connect(
        user=conf.user,
        database=conf.database,
        passwd=conf.passwd,
        host=conf.host,
        port=conf.port)

    answer = []

    cursor = connector.cursor()

    cursor.callproc('get_manufacturers')

    result = next(cursor.stored_results())
    for (manufacturer_id, manufacturer_name, manufacturer_description) in result:
        entry = {}

        entry['manufacturer_id'] = manufacturer_id
        entry['manufacturer_name'] = manufacturer_name
        entry['manufacturer_description'] = manufacturer_description

        answer.append(entry)


    connector.close()

    return json.dumps(answer), status.HTTP_200_OK
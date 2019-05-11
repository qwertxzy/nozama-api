from flask import Blueprint
from flask_api import status
import json
import mysql.connector
import conf

random = Blueprint('random', __name__)

@random.route('/random/<int:amount>')
def handle(amount):
    # amount should be > 1
    if (amount < 1):
        return '', status.HTTP_400_BAD_REQUEST

    connector = mysql.connector.connect(
        user=conf.user,
        database=conf.database,
        passwd=conf.passwd,
        host=conf.host,
        port=conf.port)

    answer = []

    cursor = connector.cursor()

    cursor.callproc('get_random_items', args=[amount])

    result = next(cursor.stored_results())

    for line in result:
        answer.append(line[0])

    cursor.close()
    return json.dumps(answer), status.HTTP_200_OK
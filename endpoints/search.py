from flask import Blueprint
from flask_api import status
import json
import mysql.connector
import conf

search = Blueprint('search', __name__)

@search.route('/search/<search_string>')
def handle(search_string):
    connector = mysql.connector.connect(
        user=conf.user,
        database=conf.database,
        passwd=conf.passwd,
        host=conf.host,
        port=conf.port)

    answer = []

    cursor = connector.cursor()

    cursor.callproc('search_item', args=['%{}%'.format(search_string)])

    result = next(cursor.stored_results())

    for line in result.fetchall():
        answer.append(line[0])

    return json.dumps(answer), status.HTTP_200_OK
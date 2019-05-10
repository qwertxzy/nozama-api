from flask import Blueprint
from flask_api import status
import json
import mysql.connector
import conf

categories = Blueprint('categories', __name__)


@categories.route('/categories')
def handle():
    connector = mysql.connector.connect(
        user=conf.user,
        database=conf.database,
        passwd=conf.passwd,
        host=conf.host,
        port=conf.port)

    answer = {}

    cursor = connector.cursor()

    # call a stored procedure to get the tags
    cursor.callproc('get_categories')

    result = next(cursor.stored_results())
    for (category_id, category_name) in result:
        answer[category_id] = category_name

    connector.close()

    return json.dumps(answer), status.HTTP_200_OK

from flask import Blueprint
from flask_api import status
import json
import mysql.connector
import conf

tags = Blueprint('tags', __name__)


@tags.route('/tags')
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
    cursor.callproc('get_tags')

    result = next(cursor.stored_results())
    for (tag_id, tag_name) in result:
        answer[tag_id] = tag_name

    connector.close()

    return json.dumps(answer), status.HTTP_200_OK

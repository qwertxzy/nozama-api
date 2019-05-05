from flask import Blueprint
from flask_api import status
import json
import conf

tags = Blueprint('tags', __name__)

@tags.route('/tags')
def handle():
    answer = {}

    cursor = conf.connector.cursor()

    #call a stored procedure to get the tags
    cursor.callproc('get_tags')

    result = next(cursor.stored_results())
    for (tag_id, tag_name) in result:
        answer[tag_id] = tag_name

    return json.dumps(answer), status.HTTP_200_OK

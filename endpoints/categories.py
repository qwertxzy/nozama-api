from flask import Blueprint
from flask_api import status
import json
import conf

categories = Blueprint('categories', __name__)

@categories.route('/categories')
def handle():
    answer = {}

    cursor = conf.connector.cursor()

    #call a stored procedure to get the tags
    cursor.callproc('get_categories')

    result = next(cursor.stored_results())
    for (category_id, category_name) in result:
        answer[category_id] = category_name

    return json.dumps(answer), status.HTTP_200_OK
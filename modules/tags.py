from flask_api import status
import json


def handle(cursor):
    cursor.execute('SELECT * FROM tag')

    answer = {}
    for (tag_id, tag_name) in cursor:
        answer[tag_id] = tag_name

    return (json.dumps(answer), status.HTTP_200_OK)

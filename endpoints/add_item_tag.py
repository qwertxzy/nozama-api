from flask import Blueprint
from flask_api import status
import mysql.connector
import conf

add_item_tag = Blueprint('add_item_tag', __name__)

@add_item_tag.route('/add_item_tag/<item_id>/<tag_name>', methods=['POST'])
def handle(item_id, tag_name):
    connector = mysql.connector.connect(
        user=conf.user,
        database=conf.database,
        passwd=conf.passwd,
        host=conf.host,
        port=conf.port)

    cursor = connector.cursor()

    return_status = cursor.callproc('add_item_tag', args=[item_id, tag_name, 0])

    if(return_status[2] == 0 or return_status[2] == 1):
        connector.close()
        return '', status.HTTP_200_OK
    elif(return_status[2] == 2):
        # item not found
        return '', status.HTTP_404_NOT_FOUND
    else:
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR
from flask import Blueprint
from flask_api import status
import mysql.connector
import conf

remove_item = Blueprint('remove_item', __name__)

@remove_item.route('/remove_item/<session_id>/<item_id>', methods=['POST'])
def handle(session_id, item_id):
    # session_ids are 16 characters long
    if (len(session_id) > 16):
        return '', status.HTTP_400_BAD_REQUEST

    connector = mysql.connector.connect(
        user=conf.user,
        database=conf.database,
        passwd=conf.passwd,
        host=conf.host,
        port=conf.port)

    cursor = connector.cursor()

    return_status = cursor.callproc('remove_from_cart', args=[session_id, item_id, 0])

    if(return_status[2] == 0):
        connector.close()
        return '', status.HTTP_200_OK
    elif(return_status[2] == 1):
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
    else:
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR
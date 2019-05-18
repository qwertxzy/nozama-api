from flask import Blueprint
from flask_api import status
import mysql.connector
import conf

delete_item = Blueprint('delete_item', __name__)

@delete_item.route('/delete_item/<session_id>/<int:item_id>', methods=['POST'])
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

    return_status = cursor.callproc('delete_item', args=[session_id, item_id, 0])

    if(return_status[2] == 0):
        # you know it
        connector.close()
        return '', status.HTTP_200_OK
    elif(return_status[2] == 1):
        # token is shit
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
    elif(return_status[2] == 2):
        # either not your item or no item at all
        connector.close()
        return '', status.HTTP_404_NOT_FOUND
    else:
        # fugg :DD
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

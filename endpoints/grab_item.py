from flask import Blueprint
from flask_api import status
import mysql.connector
import conf

grab_item = Blueprint('grab_item', __name__)


@grab_item.route('/grab_item/<session_id>/<item_id>/<amount>')
def handle(session_id, item_id, amount):
    # no adding negative amounts to your cart
    if (int(amount) < 0):
        return 'no.', status.HTTP_403_FORBIDDEN

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

    result = cursor.callproc('add_item_to_cart', args=[session_id, item_id, amount, 0])

    if (result[3] == 0):
        # 0 is a success
        connector.close()
        return '', status.HTTP_200_OK
    elif (result[3] == 1):
        # 1 means the session id could not be found
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
    elif (result[3] == 2):
        # 2 means the item_id could not be found
        connector.close()
        return '', status.HTTP_404_NOT_FOUND
    else:
        # fatal system failure
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

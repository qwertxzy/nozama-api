from flask import Blueprint
from flask_api import status
import mysql.connector
import conf

purchase = Blueprint('purchase', __name__)

@purchase.route('/purchase/<session_id>')
def handle(session_id):
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

    result = cursor.callproc('purchase_cart', args=[session_id, 0, 0])

    if(result[2] == 0):
        # 0 means success!
        connector.close()
        return '{{{}}}'.format(result[1]), status.HTTP_200_OK
    elif(result[2] == 1):
        # 1 means the user's id could not be found
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
    elif(result[2] == 2):
        # 2 means the cart was empty so making an order didn't make sense
        connector.close()
        return '', status.HTTP_400_BAD_REQUEST
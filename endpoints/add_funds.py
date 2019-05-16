from flask import Blueprint
from flask_api import status
import mysql.connector
import conf

add_funds = Blueprint('add_funds', __name__)

@add_funds.route('/add_funds/<session_id>/<amount>', methods=['POST'])
def handle(session_id, amount):
    # session_ids are 16 characters long
    if (len(session_id) > 16):
        return '', status.HTTP_400_BAD_REQUEST

    connector = mysql.connector.connect(
        user=conf.user,
        database=conf.database,
        passwd=conf.passwd,
        host=conf.host,
        port=conf.port)

    answer = {}

    cursor = connector.cursor()

    status_code = cursor.callproc('add_funds', args=[session_id, amount, 0])

    if(status_code[2] == 0):
        # all go0d
        connector.close()
        return '', status.HTTP_200_OK
    elif(status_code[2] == 1):
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
    else:
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR
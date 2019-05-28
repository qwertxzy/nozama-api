from flask import Blueprint, request
from flask_api import status
import mysql.connector
import conf


change_address = Blueprint('change_address', __name__)

@change_address.route('/change_address/<session_id>', methods=['POST'])
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

    data = request.get_json()

    city = data['city']
    zip = data['zip']
    street = data['street']

    return_status = cursor.callproc('change_address', args=[session_id, city, zip, street, 0])

    if(return_status[4] == 0):
        return '', status.HTTP_200_OK
    elif(return_status[4] == 1):
        return '', status.HTTP_401_UNAUTHORIZED
    else:
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR
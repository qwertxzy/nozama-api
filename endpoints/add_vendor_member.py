from flask import Blueprint
from flask_api import status
import mysql.connector
import conf

add_vendor_member = Blueprint('add_vendor_member', __name__)

@add_vendor_member.route('/add_vendor_member/<session_id>/<email>', methods=['POST'])
def handle(session_id, email):
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

    return_status = cursor.callproc('add_vendor_member', args=[session_id, email, 0])

    if(return_status[2] == 0):
        # you know it by now, don't you?
        connector.close()
        return '', status.HTTP_200_OK
    elif(return_status[2] == 1):
        # token is bad
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
    elif(return_status[2] == 2):
        # user email not found
        connector.close()
        return '', status.HTTP_404_NOT_FOUND
    else:
        # rip
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR
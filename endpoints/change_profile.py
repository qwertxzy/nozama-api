from flask import Blueprint, request
from flask_api import status
import mysql.connector
import conf

change_profile = Blueprint('change_profile', __name__)


@change_profile.route('/change_profile/user/<session_id>', methods=['POST'])
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

    name = data['name']
    leave_vendor = data['leave_vendor']

    return_status = cursor.callproc('change_user', args=[session_id, name, leave_vendor, 0])

    if (return_status[3] == 0):
        # success
        connector.close()
        return '', status.HTTP_200_OK
    elif (return_status[3] == 1):
        # user id not found
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
    else:
        # oh no
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

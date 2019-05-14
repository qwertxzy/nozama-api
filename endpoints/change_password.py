from flask import Blueprint, request
from flask_api import status
import mysql.connector
import conf

change_password = Blueprint('change_password', __name__)


@change_password.route('/change_password/<session_id>', methods=['POST'])
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

    #parse the request form data into variables
    password = request.form['password']

    return_status = cursor.callproc('change_password', args=[session_id, password, 0])

    if (return_status[3 == 0]):
        # all good
        connector.close()
        return '', status.HTTP_200_OK
    elif (return_status[3] == 1):
        # no user found for that token
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
    else:
        # whatever happened here, it was not anticipated
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

from flask import Blueprint, request
from flask_api import status
import json
import mysql.connector
import conf

login = Blueprint('login', __name__)


@login.route('/login', methods=['POST'])
def handle():
    connector = mysql.connector.connect(
        user=conf.user,
        database=conf.database,
        passwd=conf.passwd,
        host=conf.host,
        port=conf.port)

    answer = {}

    cursor = connector.cursor()

    # parse the request form data into variables
    email = request.form['email']
    password = request.form['password']

    result = cursor.callproc('get_token', args=[email, password, '', 0])

    connector.close()

    # the 4th argument of get_token is a return code
    if (result[3] == 0):
        # 0 means successful, so we take the returned session_id/token from the results
        answer['session_id'] = result[2]
        return json.dumps(answer), status.HTTP_200_OK
    elif (result[3] == 1):
        # 1 means the user with that email/pass combination could not be found
        return '', status.HTTP_400_BAD_REQUEST
    else:
        # unforseen troubles?
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

from flask import Blueprint, request
from flask_api import status
import mysql.connector
import conf

register = Blueprint('register', __name__)


@register.route('/register', methods=['POST'])
def handle():
    connector = mysql.connector.connect(
        user=conf.user,
        database=conf.database,
        passwd=conf.passwd,
        host=conf.host,
        port=conf.port)

    cursor = connector.cursor()

    # parse the request form data into variables
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # call a stored procedure to add a user to the db
    result = cursor.callproc('add_user', args=[username, password, email, 255])


    # the 4th entry of result is the 4th parameter, containing the out status
    if (result[3] == 0):
        # we have a 0 -> success!
        connector.close()
        return '', status.HTTP_200_OK
    elif (result[3] == 1):
        # we have a 1 -> email was not unique
        connector.close()
        return '', status.HTTP_409_CONFLICT
    else:
        # whatever happened here, it was not anticipated
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

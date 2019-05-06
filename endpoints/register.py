from flask import Blueprint, request
from flask_api import status
import conf

register = Blueprint('register', __name__)

@register.route('/register', methods=['POST'])
def handle():
    cursor = conf.connector.cursor()

    #parse the request form data into variables
    username = request.form['username']
    password = request.form['password']
    salt = request.form['salt']
    email = request.form['email']

    #call a stored procedure to add a user to the db
    result = cursor.callproc('add_user', args=[username, password, email, salt, 255])

    #the 5th entry of result is the 5th parameter, containing the out status
    if(result[4] == 0):
        #we have a 0 -> success!
        return '', status.HTTP_200_OK
    elif(result[4] == 1):
        #we have a 1 -> email was not unique
        return '', status.HTTP_409_CONFLICT
    else:
        #whatever happened here, it was not anticipated
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

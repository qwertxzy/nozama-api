from flask import Blueprint, request
from flask_api import status
from os import mkdir
import mysql.connector
import conf

add_vendor = Blueprint('add_vendor', __name__)

@add_vendor.route('/add_vendor/<session_id>', methods=['POST'])
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
    description = data['description']

    return_status = cursor.callproc('add_vendor', args=[session_id, name, description, 0, 0])

    if(return_status[4] == 0):
        # succ ess

        vendor_id = return_status[3]

        # add a directory for the images of that vendor
        mkdir(conf.web_root + '/' + conf.image_directory + '/vendor/' + str(vendor_id), 0o755)

        connector.close()
        return '', status.HTTP_200_OK
    elif(return_status[4] == 1):
        # user not found
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
    else:
        # yikes
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR
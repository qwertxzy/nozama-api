from flask import Blueprint, request
from flask_api import status
from os import listdir, path
import mysql.connector
import conf

add_item_image = Blueprint('add_item_image', __name__)

@add_item_image.route('/add_item_image/<session_id>/<item_id>', methods=['POST'])
def handle(session_id, item_id):
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

    # the actual file object
    item_image = request.files['image']

    # the extension of that file
    item_image_extension = path.splitext(item_image.filename)[1]

    # the new directory for that file
    item_image_directory = conf.web_root + '/' + conf.image_directory + '/' + item_id

    # the new file name
    item_image_name = str(len([name for name in listdir(item_image_directory)])) + item_image_extension

    # and the full path for that file
    item_image_path = item_image_directory + '/' + item_image_name

    return_status = cursor.callproc('add_item_image', args=[session_id, item_id, item_image_path, 0, 0])

    if (return_status[4] == 0):
        # all good
        item_image.save(item_image_path)
        item_image.close()

        connector.close()
        return '', status.HTTP_200_OK
    elif (return_status[4] == 1):
        # user could not be found
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
    elif (return_status[4] == 2):
        # item id could not be found or doesn't belong to the user's vendor
        connector.close()
        return '', status.HTTP_404_NOT_FOUND

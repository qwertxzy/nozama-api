from flask import Blueprint
from flask_api import status
from os import remove
import mysql.connector
import conf

remove_item_image = Blueprint('remove_item_image', __name__)

@remove_item_image.route('/remove_item_image/<session_id>/<item_id>/<file_name>', methods=['POST'])
def handle(session_id, item_id, file_name):
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

    return_status = cursor.callproc('delete_item_image', args=[session_id, item_id, file_name, 0])

    if(return_status[3] == 0):
        # all according to keikaku
        # (keikaku means plan)

        # now that the image has been deleted from the db that actually also confirmed that it was a legitimate request,
        # so we can delete the file with a good conscience
        remove(conf.web_root + '/' + conf.image_directory + '/' + item_id + '/' + file_name)

        connector.close()
        return '', status.HTTP_200_OK

    elif(return_status[3] == 1):
        # no image for that item for that vendor for that user found
        connector.close()
        return '', status.HTTP_404_NOT_FOUND
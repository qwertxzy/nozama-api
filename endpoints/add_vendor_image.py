from flask import Blueprint, request
from flask_api import status
from os import path
import mysql.connector
import conf

add_vendor_image = Blueprint('add_vendor_image', __name__)

@add_vendor_image.route('/add_vendor_image/<session_id>', methods=['POST'])
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

    #the actual file object

    vendor_image = request.files['image']

    #the extension of that file
    vendor_image_extension = path.splitext(vendor_image.filename)[1]

    # check the user's vendor
    return_status = cursor.callproc('resolve_vendor', args=[session_id, 0])

    # if the vendor id is null we're no good
    if return_status[1] == None:
        return '', status.HTTP_401_UNAUTHORIZED


    # the relative path from the web root
    vendor_image_directory = conf.image_directory + '/vendor/' + str(return_status[1]) + vendor_image_extension

    # write the relative file path into the db
    cursor.callproc('add_vendor_image', args=[return_status[1], vendor_image_directory])

    #save the image to the absolute path
    vendor_image.save(conf.web_root + '/' + vendor_image_directory)
    vendor_image.close()

    return '', status.HTTP_200_OK

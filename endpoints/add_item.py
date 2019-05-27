from flask import Blueprint, request
from flask_api import status
import mysql.connector
import json
from os import mkdir
import conf

add_item = Blueprint('add_item', __name__)


@add_item.route('/add_item/<session_id>', methods=['POST'])
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

    item_name = data['name']
    item_description = data['description']
    item_manufacturer = data['manufacturer']
    item_price = data['price']
    item_category = data['category']
    item_tags = data['tags']

    return_status = cursor.callproc('add_item', args=[session_id, item_name, item_description, item_manufacturer,
                                                      item_price, item_category, 0, 0])

    item_id = return_status[6]

    if (return_status[7] == 0):
        # 0 means good

        #add a directory for the images of that item
        mkdir(conf.web_root + '/' + conf.image_directory + '/' + str(item_id), 0o755)

        for tag in item_tags:
            cursor.callproc('add_item_tag', args=[item_id, tag, 0])


        answer = {}
        answer['item_id'] = item_id

        return json.dumps(answer), status.HTTP_200_OK
    elif (return_status[7] == 1 or return_status[7] == 2):
        # 1 means the token couldnt be resolved to a user id
        # 2 means the user isn't part of any vendor
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
    elif (return_status[7] == -1):
        # something went wrong while inserting the row into the item table
        connector.close()
        return '', status.HTTP_400_BAD_REQUEST
    else:
        # oh no
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

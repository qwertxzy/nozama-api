from flask import Blueprint, request
from flask_api import status
import mysql.connector
import conf

change_item = Blueprint('change_item', __name__)

@change_item.route('/change_item/info/<session_id>/<item_id>', methods=['POST'])
def handle_info(session_id, item_id):
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

    #call stored procedure to change core item info
    return_status = cursor.callproc('change_item', args=[session_id, item_id, item_name, item_description, item_manufacturer, item_price, item_category, 0])

    if(return_status[7] == 0):
        # no error so we continue with the tags
        cursor.callproc('delete_item_tags', args=[item_id])

        # slightly barbaric, but it'll work
        for tag in item_tags:
            cursor.callproc('add_item_tag', args=[item_id, tag, 0])

        connector.close()
        return '', status.HTTP_200_OK

    elif (return_status[7] == 1):
        # token not found or user does not belong to the items vendor
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
    elif (return_status[7] == 2 or return_status[7] == 3):
        # item not found
        connector.close()
        return '', status.HTTP_404_NOT_FOUND
    else:
        # unexpected
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

@change_item.route('/change_item/details/<session_id>/<item_id>', methods=['POST'])
def handle_details(session_id, item_id):
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

    if(cursor.callproc('check_user_item_permission', args=[session_id, item_id, 0])[2] == 0):
        # do stuff
        cursor.callproc('delete_item_details', args=[item_id])

        # add all the details
        for detail_key, detail_value in data.items():
            cursor.callproc('add_item_detail', args=[item_id, detail_key, detail_value, 0])

        connector.close()
        return '', status.HTTP_200_OK

    else:
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
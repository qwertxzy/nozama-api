from flask import Blueprint
from flask_api import status
import json
import mysql.connector
import conf

profile = Blueprint('profile', __name__)


@profile.route('/profile/<session_id>')
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

    answer = {}

    cursor = connector.cursor()

    # call a stored procedure to get information about a vendor with a given session_id
    status_code = cursor.callproc('get_profile', args=[session_id, 0])

    # the second arg is the return status
    if (status_code[1] == 0):
        # success!
        user_id = 0

        result = next(cursor.stored_results())

        for line in result.fetchall():
            user_id = line[0]
            answer['name'] = line[1]
            answer['belongs_to_vendor'] = line[2]
            answer['wallet'] = line[3]
            answer['city'] = line[4]
            answer['zip'] = line[5]
            answer['street'] = line[6]

        # initialize the cart list
        answer['cart'] = []

        # call the stored procedure
        cursor.callproc('get_profile_cart', args=[user_id])

        # nasty hacks, you know it
        result = next(cursor.stored_results())

        for line in result.fetchall():
            answer['cart'].append({'item_id': line[0], 'amount': line[1]})

        # initialize the order history list
        answer['order_history'] = []

        # call the stored procedure
        cursor.callproc('get_profile_orders', args=[user_id])

        result = next(cursor.stored_results())

        for line in result.fetchall():
            answer['order_history'].append(line[0])

        connector.close()

        return json.dumps(answer), status.HTTP_200_OK

    elif (status_code[1] == 1):
        # couldn't correlate a user_id to the token_code
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED

    else:
        # no clue what happened, probably the server's fault
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

from flask import Blueprint
from flask_api import status
import json
import conf

profile = Blueprint('profile', __name__)


@profile.route('/profile/<session_id>')
def handle(session_id):
    answer = {}

    cursor = conf.connector.cursor()

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

        return json.dumps(answer), status.HTTP_200_OK

    elif (status_code[1] == 1):
        # couldn't correlate a user_id to the token_code
        return '', status.HTTP_401_UNAUTHORIZED

    else:
        # no clue what happened, probably the server's fault
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

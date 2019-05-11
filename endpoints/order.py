from flask import Blueprint
from flask_api import status
import mysql.connector
import json
import conf

order = Blueprint('order', __name__)


@order.route('/order/<session_id>/<order_id>')
def handle(session_id, order_id):
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

    return_status = cursor.callproc('get_order', args=[session_id, order_id, 0])

    if(return_status[2] == 0):
        # success!
        result = next(cursor.stored_results())

        line = next(result)

        answer['ordered_on'] = line[0]
        answer['order_status'] = line[1]
        answer['order_total'] = line[2]
        answer['items'] = []

        cursor.callproc('get_order_items', args=[order_id])

        result = next(cursor.stored_results())

        for line in result:
            answer['items']. append({'item_id': line[0], 'amount': line[1]})

        return json.dumps(answer, default=str), status.HTTP_200_OK
    elif(return_status[2] == 1 or return_status[2] == 2):
        # user id could not be found or didn't own the order
        connector.close()
        return '', status.HTTP_401_UNAUTHORIZED
    else:
        # oh noes
        connector.close()
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR

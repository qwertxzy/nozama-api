from flask import Blueprint
from flask_api import status
import json
import conf

vendor = Blueprint('vendor', __name__)

@vendor.route('/vendor/<int:vendor_id>')
def handle(vendor_id):
    answer = {}

    cursor = conf.connector.cursor()

    #call a stored procedure to get information about a vendor
    cursor.callproc('get_vendor', args=[vendor_id])

    #if there are no returned rows, return a 404
    if cursor.rowcount == 0:
        return '{}', status.HTTP_404_NOT_FOUND

    # TODO: see item.py

    result = next(cursor.stored_results())

    for line in result.fetchall():
        answer['name'] = line[0]
        answer['description'] = line[1]
        answer['image'] = line[2]

    #call another stored procedure to get the vendor's items
    cursor.callproc('get_vendor_items', args=[vendor_id])

    answer['items'] = []

    result = next(cursor.stored_results())

    # append all returned item ids to the items list
    for line in result.fetchall():
        answer['items'].append(line[0])


    return json.dumps(answer), status.HTTP_200_OK
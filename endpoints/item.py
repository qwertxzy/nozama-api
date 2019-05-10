from flask import Blueprint
from flask_api import status
import json
import mysql.connector
import conf

item = Blueprint('item', __name__)


@item.route('/item/<int:item_id>')
def handle(item_id):
    connector = mysql.connector.connect(
        user=conf.user,
        database=conf.database,
        passwd=conf.passwd,
        host=conf.host,
        port=conf.port)

    answer = {}

    cursor = connector.cursor()

    # call a stored procedure to get information for an item
    cursor.callproc('get_item', args=[item_id])


    # TODO: find a nicer way to do this here and the other two times down
    # Basically stored results is an iterator over something(?) and we're only interested
    # in the first item, so calling next() once gives the first element of the iterable
    result = next(cursor.stored_results())

    # if there are no returned rows, return a 404
    if result.rowcount == 0:
        cursor.close()
        return '{}', status.HTTP_404_NOT_FOUND

    for line in result.fetchall():
        answer['name'] = line[0]
        answer['description'] = line[1]
        answer['vendor_id'] = line[2]
        answer['price'] = line[3]
        answer['category'] = line[4]
        answer['manufacturer'] = line[5]

    # call another stored procedure to get the item's images
    cursor.callproc('get_item_images', args=[item_id])

    answer['images'] = []

    result = next(cursor.stored_results())

    for line in result.fetchall():
        answer['images'].append(line[0])

    # call another stored procedure to get the item's tags
    cursor.callproc('get_item_tags', args=[item_id])

    answer['tags'] = []

    result = next(cursor.stored_results())

    for line in result.fetchall():
        answer['tags'].append(line[0])

    # TODO: add details(?) to the response
    connector.close()

    return json.dumps(answer), status.HTTP_200_OK

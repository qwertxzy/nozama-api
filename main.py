from flask import Flask
import mysql.connector
import conf

#import modules for request handling
import modules.tags

app = Flask(__name__)

connector = mysql.connector.connect(
    user=conf.user,
    database=conf.database,
    passwd=conf.passwd,
    host=conf.host)


@app.route("/")
def get_index():
    return "Hello world"


@app.route("/tags")
def get_tags():
    cursor = connector.cursor()

    answer = modules.tags.handle(cursor)

    cursor.close()

    return answer

from flask import Flask

#import endpoints for request handling
from endpoints.tags import tags


app = Flask(__name__)


app.register_blueprint(tags)

@app.route("/")
def get_index():
    return "Hello, this is the default route"


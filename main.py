from flask import Flask

#import endpoints for request handling
from endpoints.tags import tags
from endpoints.item import item
from endpoints.register import register

app = Flask(__name__)


app.register_blueprint(tags)
app.register_blueprint(item)
app.register_blueprint(register)

@app.route("/")
def get_index():
    return "Hello, this is the default route"


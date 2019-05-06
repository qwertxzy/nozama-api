from flask import Flask

#import endpoints for request handling
from endpoints.tags import tags
from endpoints.categories import categories
from endpoints.item import item
from endpoints.register import register
from endpoints.login import login

app = Flask(__name__)


app.register_blueprint(tags)
app.register_blueprint(categories)
app.register_blueprint(item)
app.register_blueprint(register)
app.register_blueprint(login)


@app.route("/")
def get_index():
    return "Hello, this is the default route"


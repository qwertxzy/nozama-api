from flask import Flask

# import endpoints for request handling
from endpoints.tags import tags
from endpoints.categories import categories
from endpoints.item import item
from endpoints.vendor import vendor
from endpoints.profile import profile
from endpoints.register import register
from endpoints.login import login
from endpoints.grab_item import grab_item
from endpoints.purchase import purchase
from endpoints.random import random

app = Flask(__name__)


modules = {tags, categories, item, vendor, profile, register, login,
           grab_item, purchase, random}

for m in modules:
    app.register_blueprint(m)


@app.route("/")
def get_index():
    return "Hello, this is the default route"

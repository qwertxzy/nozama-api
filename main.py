from flask import Flask

# import endpoints for request handling
from endpoints.tags import tags
from endpoints.categories import categories
from endpoints.item import item
from endpoints.vendor import vendor
from endpoints.profile import profile
from endpoints.register import register
from endpoints.login import login
from endpoints.change_password import change_password
from endpoints.grab_item import grab_item
from endpoints.purchase import purchase
from endpoints.random import random
from endpoints.order import order
from endpoints.add_item import add_item
from endpoints.add_item_image import add_item_image

app = Flask(__name__)


modules = {tags, categories, item, vendor, profile, register, login, change_password,
           grab_item, purchase, random, order, add_item, add_item_image}

for m in modules:
    app.register_blueprint(m)


@app.route("/")
def get_index():
    return "Hello, this is the default route"

from flask import Flask

# import endpoints for request handling
from endpoints.tags import tags
from endpoints.categories import categories
from endpoints.item import item
from endpoints.vendor import vendor
from endpoints.profile import profile
from endpoints.change_profile import change_profile
from endpoints.add_funds import add_funds
from endpoints.add_vendor import add_vendor
from endpoints.register import register
from endpoints.login import login
from endpoints.change_password import change_password
from endpoints.grab_item import grab_item
from endpoints.purchase import purchase
from endpoints.random import random
from endpoints.order import order
from endpoints.add_item import add_item
from endpoints.add_item_image import add_item_image
from endpoints.search import search

app = Flask(__name__)


modules = {tags, categories, item, vendor, profile, change_profile, add_funds, register, login, change_password,
           add_vendor, grab_item, purchase, random, order, add_item, add_item_image, search}

for m in modules:
    app.register_blueprint(m)


@app.route("/")
def get_index():
    return '<img src="http://progex.qwertxzy.me/images/jeff.jpg">geoff</img>'

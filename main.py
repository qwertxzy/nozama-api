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

app = Flask(__name__)


modules = {tags, categories, item, vendor, profile, register, login,
           grab_item}

for m in modules:
    app.register_blueprint(m)


@app.route("/")
def get_index():
    return "Hello, this is the default route"

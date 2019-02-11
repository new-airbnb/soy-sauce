import random
import string

from flask import Flask
from flask_cors import CORS

from utils.error_handler import generate

app = Flask(__name__)
app.secret_key = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
CORS(app)

error_codes = [400, 401, 403, 404, 405, 409, 413, 500]
for ec in error_codes:
    generate(app, ec)


@app.route("/ping", methods=["GET"])
def ping():
    return "pong!"

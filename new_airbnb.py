import random
import string

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
CORS(app)


@app.route("/ping", methods=["GET"])
def ping():
    return "pong!"

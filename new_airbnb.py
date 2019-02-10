from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "hougulubuzhuanqianguluzhuan"
CORS(app)


@app.route("/ping", methods=["GET"])
def ping():
    return "pong!"

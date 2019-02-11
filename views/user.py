import logging

from flask import Blueprint, request, jsonify
from flask_login import login_user
from pymodm.errors import ValidationError

from db.dbutils import exists
from db.models import User
from utils import error_msg
from utils.login_utils import UserLogin

logger = logging.getLogger(__name__)
user_blueprint = Blueprint("user", __name__)


def str_to_boolean(string):
    if string == "True":
        return True
    else:
        return False


@user_blueprint.route("register", methods=["POST"])
def register():
    email, password = request.form["email"], request.form["password"]
    if exists(User, {"email": email}):
        return jsonify({
            "success": 0,
            "msg": error_msg.DUPLICATE_EMAIL
        })
    else:
        try:
            user = User(email=email, password=password)
            user.save()
            return jsonify({
                "success": 1,
                "user": {
                    "email": user.email
                }
            })
        except ValidationError as ve:
            logger.warning("Failed to add new user. Exception: {}".format(ve))
            return jsonify({
                "success": 0,
                "msg": "{}: {}".format(error_msg.ILLEGAL_ARGUMENT, ",".join(list(ve.message.keys())))
            })


@user_blueprint.route("login", methods=["POST"])
def login():
    email, password, remember_me = request.form["email"], request.form["password"], request.form["remember_me"]

    if not isinstance(remember_me, bool):
        remember_me = str_to_boolean(remember_me)
    try:
        user = User.objects.get({"email": email, "password": password})
    except:
        return jsonify({
            "success": 0,
            "msg": error_msg.WRONG_PASSWORD_OR_EMAIL_ADDRESS
        })
    try:
        u = UserLogin(str(user._id), user.email, user.type)
        login_user(user=u, remember=remember_me)
        return jsonify({
            "success": 1
        })
    except Exception as e:
        logger.exception("Exception happened when trying to login. {}".format(e))
        return jsonify({
            "success": 0
        }), 500

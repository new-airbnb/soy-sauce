from flask import Blueprint, request, jsonify
from db.dbutils import exists
from db.models import User
from utils import error_msg
from pymodm.errors import ValidationError

import logging


logger = logging.getLogger(__name__)
user_blueprint = Blueprint("user", __name__)


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

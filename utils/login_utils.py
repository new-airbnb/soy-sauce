from bson import ObjectId
from flask_login import LoginManager, UserMixin

from db.models import User
from new_airbnb import app

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"


class UserLogin(UserMixin):
    def __init__(self, id, email, type):
        self.id = id
        self.email = email
        self.type = type


@login_manager.user_loader
def load_user(userid):
    try:
        _user = User.objects.get({"_id": ObjectId(userid)})
        user = UserLogin(userid, _user.email, _user.type)
        return user
    except:
        return None

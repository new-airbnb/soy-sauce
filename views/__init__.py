from new_airbnb import app
from views.user import user_blueprint

from utils import error_handler

app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')

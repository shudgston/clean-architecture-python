from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from links.context import init_context
from links.logger import get_logger

LOGGER = get_logger(__name__)
LOGIN_MANAGER = LoginManager()


def create_app():
    init_context()
    app = Flask(__name__)

    # TODO: change to read from env
    app.config['SECRET_KEY'] = 'hard to guess string'

    bootstrap = Bootstrap()
    bootstrap.init_app(app)
    LOGIN_MANAGER.init_app(app)
    LOGIN_MANAGER.login_view = 'auth.login'

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app

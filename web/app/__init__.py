from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from links.context import context
from links.entities import Bookmark, User
from links.logger import get_logger
from links.security import create_password_hash
from . import doubles

LOGGER = get_logger(__name__)
LOGIN_MANAGER = LoginManager()


def temp_testing_context():
    context.bookmark_repo = doubles.MemoryBookmarkRepo()
    context.user_repo = doubles.MemoryUserRepo()
    users = [
        User('hodor'),
        User('fred'),
    ]

    for u in users:
        u.password_hash = create_password_hash('password')
        context.user_repo.save(u)

    bookmarks = [
        Bookmark('hodorID1', 'hodor', '1: google', 'web://google.com'),
        Bookmark('hodorID2', 'hodor', '2: reddit', 'web://reddit.com'),
        Bookmark('hodorID3', 'hodor', '3: CNN', 'web://cnn.com'),
        Bookmark('hodorID4', 'hodor', '4: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam id erat sit amet ex elementum auctor quis ut sapien. Proin commodo eros', 'web://reddit.com'),
        Bookmark('fredID1', 'fred', 'altavista', 'web://altavista.com'),
    ]

    for b in bookmarks:
        context.bookmark_repo.save(b)


def create_app():
    temp_testing_context()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hard to guess string'

    bootstrap = Bootstrap()
    bootstrap.init_app(app)
    LOGIN_MANAGER.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app

from flask import render_template, redirect, url_for
from flask_login import logout_user

from links.context import context
from links.logger import get_logger
from links.usecases.users import AuthenticateUserUseCase
from . import auth
from . import presentation
from .forms import LoginForm
from .models import LoggedInUser, AnonymousUser
from .. import LOGIN_MANAGER

LOGGER = get_logger(__name__)


@LOGIN_MANAGER.user_loader
def flask_login_user_loader(user_id):
    user = context.user_repo.get(user_id)
    LOGGER.info("*** loaded user %s ***", user_id)
    if user.id is not None:
        loggedin_user = LoggedInUser()
        loggedin_user.id = user.id
        return loggedin_user

    return AnonymousUser()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        controller = presentation.AuthenticateUserController(
            AuthenticateUserUseCase(),
            presentation.AuthenticateUserPresenter(),
            presentation.AuthenticateUserView())
        return controller.handle(form)

    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

from flask import url_for, flash, redirect, render_template
from flask_login import login_user

from links.logger import get_logger
from links.usecases.interfaces import Controller, OutputBoundary, View
from .models import LoggedInUser

LOGGER = get_logger(__name__)


class AuthenticateUserController(Controller):

    def __init__(self, usecase, presenter, view):
        self.usecase = usecase
        self.presenter = presenter
        self.view = view

    def handle(self, form):
        self.view.form = form
        self.usecase.authenticate_user(form.username.data, form.password.data, self.presenter)

        is_authenticated = self.presenter.get_view_model()
        if is_authenticated:
            user = LoggedInUser()
            user.id = form.username.data
            login_user(user)

        return self.view.generate_view(is_authenticated)


class AuthenticateUserPresenter(OutputBoundary):

    def __init__(self):
        self._view_model = False

    def present(self, response_model):
        self._view_model = response_model

    def get_view_model(self):
        return self._view_model


class AuthenticateUserView(View):

    form = None

    def generate_view(self, is_authenticated):
        if is_authenticated:
            return redirect(url_for('main.index'))

        flash('Login Failed', category='danger')
        return render_template('login.html', form=self.form)

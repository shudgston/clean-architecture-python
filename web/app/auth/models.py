from flask_login import UserMixin, AnonymousUserMixin


class LoggedInUser(UserMixin):

    @property
    def name(self):
        return self.get_id()


class AnonymousUser(AnonymousUserMixin):
    pass

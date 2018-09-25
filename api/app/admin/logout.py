from flask_admin.menu import MenuLink
from flask_login import current_user


class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated

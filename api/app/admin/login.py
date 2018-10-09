from flask_admin.menu import MenuLink
from flask_login import current_user


class LoginMenuLink(MenuLink):

    def is_accessible(self):
        return not current_user.is_authenticated

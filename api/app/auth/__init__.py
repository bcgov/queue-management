from flask import abort
from flask_login import current_user
from functools import wraps

def login_required(f):
    """Determines if the access token is valid
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        print(current_user)
        print(current_user.is_authenticated)
        if current_user and current_user.is_authenticated:
        	return f(*args, **kwargs)

        else:
        	abort(401)
        
    return wrap
from flask import redirect, request, Response, abort
from flask_login import LoginManager, current_user, login_required, login_user, logout_user 

from app import models
from qsystem import application, login_manager

# somewhere to login
@application.route("/api/login/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        #Username and password can either be JSON or form based
        if "application/json" in request.content_type:
            print("Parsing JSON")
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
        else:
            print("Parsing form-data")
            username = request.form.get('username')
            password = request.form.get('password')

        if username is None or password is None:
            return abort(400)

        user = models.User.query.filter_by(username=username).first()

        if user is None:
        	return abort(400)

        if password == user.password:
            login_user(user)
            return redirect("/api/")
        else:
            return abort(401)
    else:
        if current_user.is_authenticated:
            return redirect("/api/")
            
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')

@application.route("/api/logout/")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')

# callback to reload the user object        
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()
from flask import request, jsonify, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.register"


@login_manager.unauthorized_handler
def unauthorized_callback():
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"message": "Требуется авторизация"}), 401

    return redirect(url_for(login_manager.login_view))
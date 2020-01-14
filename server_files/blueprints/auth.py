"""
Authorisation Flask routes
"""

# Library set-up
from json import dumps
from flask import Blueprint, request
from server_files.api.auth import auth_login, auth_logout, auth_passwordreset_request, auth_passwordreset_reset, auth_register

# Set up Flask Blueprint
AUTH_API = Blueprint('auth_api', __name__)

"""
Flask Routes
"""
@AUTH_API.route('/login', methods=['POST'])
def flask_auth_login():
    """Flask wrapper for auth_login"""
    email = request.form.get('email')
    password = request.form.get('password')
    return dumps(auth_login(email, password))


@AUTH_API.route('/logout', methods=['POST'])
def flask_auth_logout():
    """Flask wrapper for auth_logout"""
    token = request.form.get('token')
    return dumps(auth_logout(token))


@AUTH_API.route('/register', methods=['POST'])
def flask_auth_register():
    """Flask wrapper for auth_register"""
    email = request.form.get('email')
    password = request.form.get('password')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return dumps(auth_register(email, password, name_first, name_last))


@AUTH_API.route('/passwordreset/request', methods=['POST'])
def flask_auth_passwordreset_request():
    """Flask wrapper for auth_passwordreset_request"""
    email = request.form.get('email')
    return dumps(auth_passwordreset_request(email))


@AUTH_API.route('/passwordreset/reset', methods=['POST'])
def flask_auth_passwordreset_reset():
    """Flask wrapper for auth_passwordreset_reset"""
    reset_code = request.form.get('reset_code')
    password = request.form.get('new_password')
    return dumps(auth_passwordreset_reset(reset_code, password))

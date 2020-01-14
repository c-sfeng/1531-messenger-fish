"""
User Flask routes
"""

# Library set-up
from json import dumps
from flask import Blueprint, request
from server_files.api.users import users_all

# Set up Flask Blueprint
USERS_API = Blueprint('users_api', __name__)


"""
Flask Routes
"""
@USERS_API.route('/all', methods=['GET'])
def flask_users_profiles_uploadphoto():
    """Flask wrapper for users_all"""
    token = request.args.get('token')
    return dumps(users_all(token))

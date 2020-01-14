"""
User functions and Flask routes
"""

# Library set-up
from json import dumps
from flask import Blueprint, request
from server_files.api.user import user_profile, user_profile_setemail, user_profile_sethandle, user_profile_setname, user_profiles_uploadphoto

# Set up Flask Blueprint
USER_API = Blueprint('user_api', __name__)

"""
Flask Routes
"""
@USER_API.route('/profile', methods=['GET'])
def flask_user_profile():
    """Flask wrapper for user_profile"""
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    return dumps(user_profile(token, u_id))


@USER_API.route('/profile/setname', methods=['PUT'])
def flask_user_profile_setname():
    """Flask wrapper for user_setname"""
    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')
    return dumps(user_profile_setname(token, name_first, name_last))


@USER_API.route('/profile/setemail', methods=['PUT'])
def flask_user_profile_setemail():
    """Flask wrapper for user_setemail"""
    token = request.form.get('token')
    email = request.form.get('email')
    return dumps(user_profile_setemail(token, email))


@USER_API.route('/profile/sethandle', methods=['PUT'])
def flask_user_profile_sethandle():
    """Flask wrapper for user_sethandle"""
    token = request.form.get('token')
    handle_str = request.form.get('handle_str')
    return dumps(user_profile_sethandle(token, handle_str))


@USER_API.route('/profiles/uploadphoto', methods=['POST'])
def flask_user_profiles_uploadphoto():
    """Flask wrapper for user_profiles_uploadphoto"""
    token = request.form.get('token')
    img_url = request.form.get('img_url')
    x_start = request.form.get('x_start')
    y_start = request.form.get('y_start')
    x_end = request.form.get('x_end')
    y_end = request.form.get('y_end')
    return user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)

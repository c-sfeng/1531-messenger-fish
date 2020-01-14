"""
Echo Flask routes
"""

# Library set-up
from json import dumps
from flask import Blueprint, request
from server_files.api.echo import echo_post, echo_get

# Set up Flask Blueprint
ECHO_API = Blueprint('echo_api', __name__)

"""
Flask Routes
"""
@ECHO_API.route('/post', methods=['POST'])
def flask_echo_post():
    """Flask wrapper for echo_post"""
    echo = request.form.get('echo')
    return dumps(echo_post(echo))


@ECHO_API.route('/get', methods=['GET'])
def flask_echo_get():
    """Flask wrapper for echo_get"""
    echo = request.args.get('echo')
    return dumps(echo_get(echo))

"""
Channels Flask routes
"""

# Library set-up
from json import dumps
from flask import Blueprint, request
from server_files.api.channels import channels_list, channels_listall, channels_create

# Set up Flask Blueprint
CHANNELS_API = Blueprint('channels_api', __name__)


"""
Flask Routes
"""
@CHANNELS_API.route('/list', methods=['GET'])
def flask_channels_list():
    """Flask wrapper for channels_list"""
    token = request.args.get('token')
    return dumps(channels_list(token))


@CHANNELS_API.route('/listall', methods=['GET'])
def flask_channels_listall():
    """Flask wrapper for channels_listall"""
    token = request.args.get('token')
    return dumps(channels_listall(token))


@CHANNELS_API.route('/create', methods=['POST'])
def flask_channels_create():
    """Flask wrapper for channels_create"""
    token = request.form.get('token')
    name = request.form.get('name')
    is_public = request.form.get('is_public')
    return dumps(channels_create(token, name, is_public))

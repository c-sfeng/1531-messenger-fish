"""
Standup Flask routes
"""

# Library set-up
from json import dumps
from flask import Blueprint, request
from server_files.api.standup import standup_start, standup_active, standup_send

# Set up Flask Blueprint
STANDUP_API = Blueprint('standup_api', __name__)

"""
Flask Routes
"""


@STANDUP_API.route('/start', methods=['POST'])
def flask_standup_start():
    """Flask wrapper for standup_start"""
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    length = request.form.get('length')
    return dumps(standup_start(token, channel_id, length))


@STANDUP_API.route('/active', methods=['GET'])
def flask_standup_active():
    """Flask wrapper for standup_active"""
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return dumps(standup_active(token, channel_id))


@STANDUP_API.route('/send', methods=['POST'])
def flask_standup_send():
    """Flask wrapper for standup_send"""
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')
    return dumps(standup_send(token, channel_id, message))

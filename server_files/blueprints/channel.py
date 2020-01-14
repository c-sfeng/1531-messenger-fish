"""
Channel Flask routes
"""

# Library set-up
from json import dumps
from flask import Blueprint, request
from server_files.api.channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join, channel_addowner, channel_removeowner

# Set up Flask Blueprint
CHANNEL_API = Blueprint('channel_api', __name__)


"""
Flask Routes
"""
@CHANNEL_API.route('/invite', methods=['POST'])
def flask_channel_invite():
    """Flask wrapper for channel_invite"""
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    return dumps(channel_invite(token, channel_id, u_id))


@CHANNEL_API.route('/details', methods=['GET'])
def flask_channel_details():
    """Flask wrapper for channel_details"""
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    return dumps(channel_details(token, channel_id))


@CHANNEL_API.route('/messages', methods=['GET'])
def flask_channel_messages():
    """Flask wrapper for channel_messages"""
    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    return dumps(channel_messages(token, channel_id, start))


@CHANNEL_API.route('/leave', methods=['POST'])
def flask_channel_leave():
    """Flask wrapper for channel_leave"""
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    return dumps(channel_leave(token, channel_id))


@CHANNEL_API.route('/join', methods=['POST'])
def flask_channel_join():
    """Flask wrapper for channel_join"""
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    return dumps(channel_join(token, channel_id))


@CHANNEL_API.route('/addowner', methods=['POST'])
def flask_channel_addowner():
    """Flask wrapper for channel_addowner"""
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    return dumps(channel_addowner(token, channel_id, u_id))


@CHANNEL_API.route('/removeowner', methods=['POST'])
def flask_channel_removeowner():
    """Flask wrapper for channel_removeowner"""
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    u_id = request.form.get('u_id')
    return dumps(channel_removeowner(token, channel_id, u_id))

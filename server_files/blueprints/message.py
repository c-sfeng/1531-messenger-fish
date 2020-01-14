"""
Message Flask routes
"""

# Library set-up
from json import dumps
from flask import Blueprint, request
from server_files.api.message import message_edit, message_pin, message_react, message_remove, message_send, message_sendlater, message_unpin, message_unreact

# Set up Flask Blueprint
MESSAGE_API = Blueprint('message_api', __name__)


"""
Flask Routes
"""
@MESSAGE_API.route('/sendlater', methods=['POST'])
def flask_message_sendlater():
    """Flask wrapper for message_sendlater"""
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')
    time_sent = request.form.get('time_sent')
    print("")
    print("")
    print("")
    print(time_sent)
    print("")
    return dumps(message_sendlater(token, channel_id, message, time_sent))


@MESSAGE_API.route('/send', methods=['POST'])
def flask_messsage_send():
    """Flask wrapper for message_send"""
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    message = request.form.get('message')
    return dumps(message_send(token, channel_id, message))


@MESSAGE_API.route('/remove', methods=['DELETE'])
def flask_message_remove():
    """Flask wrapper for message_remove"""
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    return dumps(message_remove(token, message_id))


@MESSAGE_API.route('/edit', methods=['PUT'])
def flask_message_edit():
    """Flask wrapper for message_edit"""
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    message = request.form.get('message')
    return dumps(message_edit(token, message_id, message))


@MESSAGE_API.route('/react', methods=['POST'])
def flask_message_react():
    """Flask wrapper for message_react"""
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    react_id = request.form.get('react_id')
    return dumps(message_react(token, message_id, react_id))


@MESSAGE_API.route('/unreact', methods=['POST'])
def flask_message_unreact():
    """Flask wrapper for message_unreact"""
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    react_id = request.form.get('react_id')
    return dumps(message_unreact(token, message_id, react_id))


@MESSAGE_API.route('/pin', methods=['POST'])
def flask_message_pin():
    """Flask wrapper for message_pin"""
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    return dumps(message_pin(token, message_id))


@MESSAGE_API.route('/unpin', methods=['POST'])
def flask_message_unpin():
    """Flask wrapper for message_unpin"""
    token = request.form.get('token')
    message_id = request.form.get('message_id')
    return dumps(message_unpin(token, message_id))

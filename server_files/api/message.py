"""
Message functions
"""

# Library set-up
from datetime import datetime
from server_files.data import database
from server_files.util import jwt_handler, validator, json_time_translator
from server_files.exceptions.my_exceptions import AccessError, ValueError
from server_files.exceptions.err_msgs import\
    INVALID_TOKEN, INVALID_MESSAGE, INVALID_CHANNEL, MESSAGE_TIME_INVALID, MESSAGE_SEND_NO_AUTH,\
    MESSAGE_REMOVE_NOT_EXIST, MESSAGE_EDIT_NO_AUTH, MESSAGE_EDIT_NOT_EXIST,\
    CHANNEL_CANT_VIEW_DETAIL, INVALID_REACT, MESSAGE_ALREADY_REACTED, MESSAGE_NOT_REACTED,\
    MESSAGE_PIN_NOT_EXIST, MESSAGE_PIN_NO_AUTH, MESSAGE_ALREADY_PINNED, MESSAGE_UNPIN_NOT_EXIST,\
    MESSAGE_UNPIN_NO_AUTH, MESSAGE_NOT_PINNED
from server_files.util.constants import OWNER, ADMIN

"""
API Functions
"""


def message_sendlater(token, channel_id, message, time_sent):
    """
    Send a message from authorised_user to the channel specified by channel_id
    """
    # Validate data
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)
    if not validator.is_valid_message(message):
        raise ValueError(INVALID_MESSAGE)

    # Convert token to u_id
    u_id = jwt_handler.decode_token(token)
    # Check channel exists
    channel = database.get_channel_by_id(channel_id)
    if channel is None:
        raise ValueError(INVALID_CHANNEL)

    # Read time_sent
    time_to_send = json_time_translator.timestamp_to_datetime(time_sent)
    # Check time_to_send is not in the past
    if time_to_send <= datetime.utcnow():
        raise ValueError(MESSAGE_TIME_INVALID)

    if u_id not in channel["auth_ids"]:
        raise AccessError(MESSAGE_SEND_NO_AUTH)

    # Create message
    message_id = database.add_message({
        "u_id": u_id,
        "message": message,
        "channel_id": int(channel_id),
        "time_created": json_time_translator.datetime_to_json(time_to_send),
        "is_pinned": False,
        "reacts": []
    })
    # Insert into channel's list of messages in order of time
    message_id_list = channel["messages"]

    inserted = False
    for i in reversed(range(len(message_id_list))):
        json_time = database.get_message_by_id(
            message_id_list[i])["time_created"]
        timestamp = json_time_translator.json_to_timestamp(json_time)
        if timestamp <= int(float(time_sent)):
            message_id_list.insert(i + 1, message_id)
            inserted = True
            break
    if inserted is False:
        message_id_list.insert(0, message_id)
    database.update_channel_by_id(channel_id, {
        "messages": message_id_list
    })
    return {
        "message_id": message_id
    }


def message_send(token, channel_id, message):
    """
    Send a message from authorised_user to the channel specified by channel_id
    """
    # Validate data
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)
    if not validator.is_valid_message(message):
        raise ValueError(INVALID_MESSAGE)
    # Convert token to u_id
    u_id = jwt_handler.decode_token(token)
    # Check u_id is authorised
    channel = database.get_channel_by_id(channel_id)
    if channel is None:
        raise ValueError(INVALID_CHANNEL)

    if u_id not in channel["auth_ids"]:
        raise AccessError(MESSAGE_SEND_NO_AUTH)

    # Create message
    time_sent = datetime.utcnow()
    message_id = database.add_message({
        "u_id": u_id,
        "message": message,
        "channel_id": int(channel_id),
        "time_created": json_time_translator.datetime_to_json(time_sent),
        "is_pinned": False,
        "reacts": []
    })
    # Add to channel's list of messages
    message_id_list = channel["messages"]

    inserted = False
    for i in reversed(range(len(message_id_list))):
        json_time = database.get_message_by_id(
            message_id_list[i])["time_created"]
        timestamp = json_time_translator.json_to_timestamp(json_time)
        if timestamp <= json_time_translator.datetime_to_timestamp(time_sent):
            message_id_list.insert(i + 1, message_id)
            inserted = True
            break
    if inserted is False:
        message_id_list.insert(0, message_id)

    database.update_channel_by_id(channel_id, {
        "messages": message_id_list
    })
    return {
        "message_id": message_id
    }


def message_remove(token, message_id):
    """
    Given a message_id for a message, this message is removed from the chxnel
    """
    # Validate token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    if not isinstance(message_id, int):
        message_id = int(message_id)

    # Convert token to u_id
    u_id = jwt_handler.decode_token(token)

    # Check u_id is authorised
    user = database.get_user_by_id(u_id)
    message = database.get_message_by_id(message_id)
    if message is None:
        raise ValueError(MESSAGE_REMOVE_NOT_EXIST)

    channel_id = message["channel_id"]
    channel = database.get_channel_by_id(channel_id)
    # if sender of message
    if u_id == message["u_id"] or\
            user["permission"] in [OWNER, ADMIN] or\
            u_id in channel["owner_ids"]:
        # Delete message from database
        database.delete_message_by_id(message_id)
        # Delete message from channel
        channel["messages"].remove(message_id)
        database.update_channel_by_id(channel_id, channel)
        return {}
    raise AccessError(MESSAGE_EDIT_NO_AUTH)


def message_edit(token, message_id, message):
    """Given a message, update it's text with new text"""
    # Validate token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    # If the message is empty, perform deletion instead
    if message == "":
        return message_remove(token, message_id)

    if not validator.is_valid_message(message):
        raise ValueError(INVALID_MESSAGE)

    # Convert token to u_id
    u_id = jwt_handler.decode_token(token)

    user = database.get_user_by_id(u_id)
    message_dict = database.get_message_by_id(message_id)
    if message_dict is None:
        raise ValueError(MESSAGE_EDIT_NOT_EXIST)

    channel_id = message_dict["channel_id"]
    channel = database.get_channel_by_id(channel_id)

    # Check if user can edit this message
    if u_id == message_dict["u_id"] or user["permission"] in [OWNER, ADMIN] \
            or u_id in channel["owner_ids"]:
        database.update_message_by_id(message_id, {
            "message": message
        })
        return {}
    raise AccessError(MESSAGE_EDIT_NO_AUTH)


def message_react(token, message_id, react_id):
    """
    Given a message within a channel the authorised user is part of, add a
    "react" to that particular message
    """
    # Validate
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    # Decode token
    u_id = jwt_handler.decode_token(token)

    # Change react_id to an integer
    if not isinstance(react_id, int):
        react_id = int(react_id)
    if not isinstance(message_id, int):
        message_id = int(message_id)

    # Validate data
    message = database.get_message_by_id(message_id)
    channel = database.get_channel_by_id(message["channel_id"])

    if u_id not in channel["auth_ids"]:
        raise AccessError(CHANNEL_CANT_VIEW_DETAIL)

    if react_id != 1:
        print(react_id)
        raise ValueError(INVALID_REACT)

    react_id_exists = False
    for react in message["reacts"]:
        if react_id == react["react_id"]:
            react_id_exists = True
            if u_id in react["u_id"]:
                raise ValueError(MESSAGE_ALREADY_REACTED)
            break

    # Add react to message
    react_list = message["reacts"]
    if not react_id_exists:
        react_list.append({"react_id": react_id, "u_id": [u_id]})
    else:
        for react in react_list:
            if react_id == react["react_id"]:
                react["u_id"].append(u_id)
                break

    database.update_message_by_id(message_id, {
        "reacts": react_list
    })
    return {}


def message_unreact(token, message_id, react_id):
    """
    Given a message within a channel the authorised user is part of, remove a
    "react" to that particular message
    """
    # Validate
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)
    # Decode token
    u_id = jwt_handler.decode_token(token)

    # Change react_id to an integer
    if not isinstance(react_id, int):
        react_id = int(react_id)
    if not isinstance(message_id, int):
        message_id = int(message_id)

    # Validate data
    message = database.get_message_by_id(message_id)
    channel = database.get_channel_by_id(message["channel_id"])

    if u_id not in channel["auth_ids"]:
        raise AccessError(CHANNEL_CANT_VIEW_DETAIL)

    if react_id != 1:
        print(react_id)
        raise ValueError(INVALID_REACT)

    react_list = message["reacts"]
    react_found = False
    for react in react_list:
        if react_id == react["react_id"] and u_id in react["u_id"]:
            react_found = True
            break

    if not react_found:
        raise ValueError(MESSAGE_NOT_REACTED)

    # Remove react from message
    for react in react_list:
        if react_id == react["react_id"]:
            react["u_id"].remove(u_id)

    database.update_message_by_id(message_id, {
        "reacts": react_list
    })
    return {}


def message_pin(token, message_id):
    """
    Given a message within a channel, mark it as "pinned" to be given special
    display treatment by the frontend
    """
    # Validate token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    # Decode token
    u_id = jwt_handler.decode_token(token)

    user = database.get_user_by_id(u_id)
    message = database.get_message_by_id(message_id)
    if message is None:
        raise ValueError(MESSAGE_PIN_NOT_EXIST)
    channel = database.get_channel_by_id(message["channel_id"])

    if user["permission"] not in [OWNER, ADMIN] \
            and u_id not in channel["owner_ids"]:
        raise ValueError(MESSAGE_PIN_NO_AUTH)

    # Checking data
    if u_id not in channel["auth_ids"]:
        raise AccessError(CHANNEL_CANT_VIEW_DETAIL)

    if message["is_pinned"] is True:
        raise ValueError(MESSAGE_ALREADY_PINNED)

    # Pinning message
    database.update_message_by_id(message_id, {
        "is_pinned": True
    })
    return {}


def message_unpin(token, message_id):
    """Given a message within a channel, remove it's mark as unpinned"""
    # Validate token
    if not validator.is_valid_token(token):
        raise ValueError(INVALID_TOKEN)

    # Decode token
    u_id = jwt_handler.decode_token(token)

    user = database.get_user_by_id(u_id)
    message = database.get_message_by_id(message_id)
    if message is None:
        raise ValueError(MESSAGE_UNPIN_NOT_EXIST)
    channel = database.get_channel_by_id(message["channel_id"])

    if user["permission"] not in [OWNER, ADMIN] \
            and u_id not in channel["owner_ids"]:
        raise AccessError(MESSAGE_UNPIN_NO_AUTH)

    # Checking data
    if u_id not in channel["auth_ids"]:
        raise AccessError(CHANNEL_CANT_VIEW_DETAIL)

    if message["is_pinned"] is False:
        raise ValueError(MESSAGE_NOT_PINNED)

    # Unpinning message
    database.update_message_by_id(message_id, {
        "is_pinned": False
    })
    return {}

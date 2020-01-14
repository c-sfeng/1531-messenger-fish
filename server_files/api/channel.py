"""
Channel functions
"""

# Library set-up
from datetime import datetime
from server_files.exceptions.my_exceptions import AccessError, ValueError
from server_files.exceptions.err_msgs import\
    INVALID_TOKEN, INVALID_CHANNEL, INVALID_USER, CHANNEL_INV_NO_AUTH, CHANNEL_ALREADY_JOINED,\
    CHANNEL_CANT_VIEW_DETAIL, CHANNEL_CANT_VIEW_MSG, CHANNEL_NO_MORE_MSG, NOT_IN_CHANNEL,\
    CHANNEL_ADD_OWNER_NO_AUTH, CHANNEL_ALREADY_OWNER, CHANNEL_DEL_OWNER_NO_AUTH, CHANNEL_NOT_OWNER
from server_files.data import database
from server_files.util import jwt_handler, validator, json_time_translator
from server_files.util.constants import OWNER, ADMIN, MEMBER

"""
API Functions
"""
def channel_invite(token, channel_id, u_id):
    """Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately"""
    # Convert channel_id and u_id to integer
    channel_id = int(channel_id)
    u_id = int(u_id)

    # Validate token, channel and user
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)
    if not validator.is_valid_channel(channel_id):
        raise ValueError(INVALID_CHANNEL)
    if not validator.is_valid_user(u_id):
        raise ValueError(INVALID_USER)

    # Find invitor
    invitor_id = jwt_handler.decode_token(token)

    # Locate channel in database
    channel = database.get_channel_by_id(channel_id)

    # Check that the invitor is authorised
    auth_list = channel["auth_ids"]

    if invitor_id not in auth_list:
        raise AccessError(CHANNEL_INV_NO_AUTH)
    if u_id in auth_list:
        raise ValueError(CHANNEL_ALREADY_JOINED)
    auth_list.append(u_id)
    database.update_channel_by_id(channel_id, {
        "auth_ids": auth_list
    })
    return {}

def channel_details(token, channel_id):
    """Given a Channel with ID channel_id that the authorised user is part of,
    provide basic details about the channel"""
    # Validate token and channel
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)
    if not validator.is_valid_channel(channel_id):
        raise ValueError(INVALID_CHANNEL)

    # Find user in database
    u_id = jwt_handler.decode_token(token)

    # Locate in database
    channel = database.get_channel_by_id(channel_id)
    user = database.get_user_by_id(u_id)

    # Check user is authorised
    if u_id not in channel["auth_ids"] and user["permission"] == MEMBER:
        raise AccessError(CHANNEL_CANT_VIEW_DETAIL)

    # Compile channel details
    owner_list = channel["owner_ids"]
    auth_list = channel["auth_ids"]
    owner_list_with_details = []
    auth_list_with_details = []
    for owner_id in owner_list:
        owner = database.get_user_by_id(owner_id)
        owner_list_with_details.append({
            "u_id": owner_id,
            "name_first": owner["name_first"],
            "name_last": owner["name_last"],
            "profile_img_url": owner["profile_img_url"]})
    for auth_id in auth_list:
        auth = database.get_user_by_id(auth_id)
        auth_list_with_details.append({
            "u_id": auth_id,
            "name_first": auth["name_first"],
            "name_last": auth["name_last"],
            "profile_img_url": auth["profile_img_url"]})
    return {
        "name": channel["name"],
        "owner_members": owner_list_with_details,
        "all_members": auth_list_with_details
    }


def channel_messages(token, channel_id, start):
    """Given a Channel with ID channel_id that the authorised user is part of,
    return up to 50 messages between index "start" and "start + 50". Message
    with index 0 is the most recent message in the channel. This function
    returns a new index "end" which is the value of "start + 50", or, if this
    function has returned the least recent messages in the channel, returns -1
    in "end" to indicate there are no more messages to load after this
    return."""
    # Convert 'start' to an integer
    start = int(start)

    # Validate token and channel ID
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)
    if not validator.is_valid_channel(channel_id):
        raise ValueError(INVALID_CHANNEL)

    # Locate channel
    channel = database.get_channel_by_id(channel_id)

    # Validate that token user is in channel
    u_id = jwt_handler.decode_token(token)
    if u_id not in channel["auth_ids"]:
        raise AccessError(CHANNEL_CANT_VIEW_MSG)

    # Validate messages exist
    total_messages = len(channel['messages'])
    if total_messages <= 0:
        return {
            "messages": [],
            "start": start,
            "end": -1
        }

    # Validate start point
    if start > (total_messages - 1) or start < 0:
        raise ValueError(CHANNEL_NO_MORE_MSG)

    # Find index for the most recent message (reference list backwards)
    start_index = len(channel['messages']) - 1 - start
    # Get all recent messages up to 50
    messages = []
    end = start + 49
    for msg_num in range(50):
        index = start_index - msg_num
        # If there are less than 50 msgs
        if index < 0:
            end = -1
            break

        # Get message object
        message_id = channel['messages'][index]
        message = database.get_message_by_id(message_id)

        # If message is sent later or not there
        if message is None or\
                json_time_translator.json_to_datetime(message["time_created"]) >= datetime.utcnow():
            continue

        # Create output-able list of reacts
        react_list = []
        reacted_ids = []
        all_reacts = database.get_all_reacts(message_id)
        react_id = 1
        for react in all_reacts:
            is_this_user_reacted = False
            if react["react_id"] == react_id:
                reacted_ids.extend(react["u_id"])
                if u_id in react["u_id"]:
                    is_this_user_reacted = True
                # Only add the reaction if it has at least one count of a user
                react_list.append({
                    "react_id": react_id,
                    "u_ids": reacted_ids,
                    "is_this_user_reacted": is_this_user_reacted
                })

        # print(message["time_created"])
        # print(json_time_translator.json_to_datetime(message["time_created"]))
        # print(json_time_translator.json_to_timestamp(message["time_created"]))
        # Append to file
        messages.append({
            "message_id": message_id,
            "u_id": message["u_id"],
            "message": message["message"],
            "time_created": json_time_translator.json_to_timestamp(message["time_created"]),
            "reacts": react_list,
            "is_pinned": message["is_pinned"]
        })

    return {
        "messages": messages,
        "start": start,
        "end": end
    }


def channel_leave(token, channel_id):
    """Given a channel ID, the user removed as a member of this channel"""
    # Validate token and channel ID
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)
    if not validator.is_valid_channel(channel_id):
        raise ValueError(INVALID_CHANNEL)

    # Convert token to u_id
    u_id = jwt_handler.decode_token(token)


    # Locate channel
    channel = database.get_channel_by_id(channel_id)

    # Validate user is in channel
    auth_list = channel["auth_ids"]
    if u_id not in auth_list:
        raise AccessError(NOT_IN_CHANNEL)

    # Remove user from auth_list
    auth_list.remove(u_id)
    database.update_channel_by_id(channel_id, {
        "auth_ids": auth_list
    })

    # If owner, remove from owner_list
    owner_list = channel["owner_ids"]
    if u_id in owner_list:
        owner_list.remove(u_id)
        database.update_channel_by_id(channel_id, {
            "owner_ids": owner_list
        })

    return {}


def channel_join(token, channel_id):
    """Given a channel_id of a channel that the authorised user can join, adds
    them to that channel"""
    # Validate token and channel ID
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)
    if not validator.is_valid_channel(channel_id):
        raise ValueError(INVALID_CHANNEL)

    # Convert token to u_id
    u_id = jwt_handler.decode_token(token)
    user = database.get_user_by_id(u_id)

    # Locate channel in database
    channel = database.get_channel_by_id(channel_id)

    # If channel is private
    if not channel["is_public"] and user["permission"] == MEMBER:
        # If the user is not an admin/owner
        raise AccessError(CHANNEL_CANT_VIEW_DETAIL)

    # Add user to authorised users in channel
    auth_list = channel["auth_ids"]
    if u_id not in auth_list:
        auth_list.append(u_id)
        database.update_channel_by_id(channel_id, {
            "auth_ids": auth_list
        })
    else:
        raise ValueError(CHANNEL_ALREADY_JOINED)

    return {}


def channel_addowner(token, channel_id, u_id):
    """Make user with user id u_id an owner of this channel"""
    # Convert channel_id and u_id to integer
    channel_id = int(channel_id)
    u_id = int(u_id)

    # Validate token, channel and user
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)
    if not validator.is_valid_channel(channel_id):
        raise ValueError(INVALID_CHANNEL)
    if not validator.is_valid_user(u_id):
        raise ValueError(INVALID_USER)

    # Locate channel and user in database
    channel = database.get_channel_by_id(channel_id)
    auth_user_id = jwt_handler.decode_token(token)
    auth_user = database.get_user_by_id(auth_user_id)

    # Check auth_user permissions
    if auth_user["permission"] not in [OWNER, ADMIN] or\
            auth_user_id not in channel["owner_ids"]:
        raise AccessError(CHANNEL_ADD_OWNER_NO_AUTH)


    # Add user to auth_ids
    auth_list = channel["auth_ids"]
    if u_id not in auth_list:
        auth_list.append(u_id)
        database.update_channel_by_id(channel_id, {
            "auth_ids": auth_list
        })

    # Add user to owner_ids
    owner_list = channel["owner_ids"]
    if u_id in owner_list:
        raise ValueError(CHANNEL_ALREADY_OWNER)
    owner_list.append(u_id)
    database.update_channel_by_id(channel_id, {
        "owner_ids": owner_list
    })

    return {}


def channel_removeowner(token, channel_id, u_id):
    """Remove user with user id u_id an owner of this channel"""
    # Convert channel_id and u_id to integer
    channel_id = int(channel_id)
    u_id = int(u_id)

    # Validate token, channel and user
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)
    if not validator.is_valid_channel(channel_id):
        raise ValueError(INVALID_CHANNEL)
    if not validator.is_valid_user(u_id):
        raise ValueError(INVALID_USER)

    # Locate channel and user in database
    channel = database.get_channel_by_id(channel_id)
    auth_user_id = jwt_handler.decode_token(token)
    auth_user = database.get_user_by_id(auth_user_id)
    owner_list = channel["owner_ids"]

    if auth_user["permission"] not in [OWNER, ADMIN] or\
            auth_user_id not in channel["owner_ids"]:
        raise AccessError(CHANNEL_DEL_OWNER_NO_AUTH)

    # Check that the added_user is currently an owner
    if u_id not in owner_list:
        raise ValueError(CHANNEL_NOT_OWNER)

    # Remove user from owner_ids
    owner_list.remove(u_id)
    database.update_channel_by_id(channel_id, {
        "owner_ids": owner_list
    })

    return {}

"""
Channels functions
"""

# Library set-up
from server_files.data import database
from server_files.util import jwt_handler, validator
from server_files.exceptions.my_exceptions import AccessError, ValueError
from server_files.exceptions.err_msgs import\
    INVALID_TOKEN, CHANNEL_LONG_NAME


"""
API Functions
"""


def channels_list(token):
    """Provide a list of all channels (and their associated details) that
    the authorised user is part of"""
    # Check validity of token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    # Convert token to u_id
    u_id = jwt_handler.decode_token(token)
    # Get channels token is authorised in
    result = []
    for channel in database.get_all_channels():
        if (u_id in channel["auth_ids"] or u_id in channel["owner_ids"]):
            result.append({
                "channel_id": channel["channel_id"],
                "name": channel["name"]
            })

    return {
        "channels": result
    }


def channels_listall(token):
    """Provide a list of all channels (and their associated details)"""
    # Check validity of token
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    channels = database.get_all_channels()
    result = []
    for channel in channels:
        result.append(
            {"channel_id": channel["channel_id"], "name": channel["name"]})
    return {
        "channels": result
    }


def channels_create(token, name, is_public):
    """Creates a new channel with that name that is either a public or private channel"""
    # Convert is_public to boolean
    is_public = is_public.lower() in ("true", "yes", "t", "1")

    # Validate token & data
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)
    if not validator.is_valid_channel_name(name):
        raise ValueError(CHANNEL_LONG_NAME)

    # Convert token to u_id
    u_id = jwt_handler.decode_token(token)

    # Create channel and get ID
    channel_id = database.add_channel({
        "name": name,
        "messages": [],
        "is_public": is_public,
        "owner_ids": [u_id],
        "auth_ids": [u_id]
    })
    return {
        "channel_id": channel_id
    }

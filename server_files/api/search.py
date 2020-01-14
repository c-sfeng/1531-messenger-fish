"""
Search function
"""

# Library set-up
from server_files.data import database
from server_files.util import jwt_handler, validator
from server_files.exceptions.my_exceptions import AccessError
from server_files.exceptions.err_msgs import INVALID_TOKEN
from server_files.util import json_time_translator

"""
API Functions
"""

def get_react_list(message, u_id):
    """Returns a list of reacts for given message"""
    react_list = []
    for react in message["reacts"]:
        is_this_user_reacted = False
        if u_id in react["u_id"]:
            is_this_user_reacted = True
        react_list.append({
            "react_id": react["react_id"],
            "u_ids": react["u_id"],
            "is_this_user_reacted": is_this_user_reacted
        })
    return react_list


def search(token, query_str):
    """Given a query string, return a collection of messages in all of the
    channels that the user has joined that match the query"""
    if not validator.is_valid_token(token):
        raise AccessError(INVALID_TOKEN)

    # If the query is whitespace
    if (query_str.isspace() or len(query_str) == 0):
        return {
            "messages": []
        }

    u_id = jwt_handler.decode_token(token)

    result = []
    for channel in database.get_all_channels():
        if u_id in channel["auth_ids"]:
            for message_id in channel["messages"]:
                message = database.get_message_by_id(message_id)
                if query_str in message["message"]:
                    # Create output-able list of reacts
                    react_list = get_react_list(message, u_id)
                    # Write to file
                    time_created = json_time_translator.json_to_timestamp(message["time_created"])
                    result_entry = {
                        "message_id": message_id,
                        "u_id": message["u_id"],
                        "message": message["message"],
                        "time_created": time_created,
                        "reacts": react_list,
                        "is_pinned": message["is_pinned"]
                    }
                    result.append(result_entry)
    return {
        "messages": result
    }

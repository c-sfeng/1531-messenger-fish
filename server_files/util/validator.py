# LIbrary set-up
import re
from server_files.data import database
from server_files.util import jwt_handler

"""
Validation Functions
"""
def is_valid_email(email):
    """Returns whether or not an email is valid"""
    if isinstance(email, str) and re.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
        return True
    return False

def is_valid_password(password):
    """Returns whether or not a password is of sufficient length"""
    if len(password) >= 5:
        return True
    return False

def is_valid_name(name):
    """Returns whether or not a name is of appropriate length"""
    if len(name) > 0 and len(name) <= 50:
        return True
    return False

def is_valid_token(token):
    """Returns whether or not a token is valid: that the signature is valid and that
    it is an actively listed token under the user's data file"""
    u_id = jwt_handler.decode_token(token)
    if u_id is None:
        return False
    user = database.get_user_by_id(u_id)
    if user is None:
        return False
    for active_token in user["tokens"]:
        if active_token == token:
            return True
    return False

def is_valid_user(u_id):
    """Returns whether or not a user id id valid"""
    if database.get_user_by_id(u_id) is None:
        return False
    return True

def is_valid_channel_name(channel_name):
    """Returns whether or not a channel name is of appropriate length"""
    if len(channel_name) > 20:
        return False
    return True

def is_valid_handle(handle):
    """Returns if a handle string is of appropriate name"""
    if len(handle) < 1 or len(handle) > 20:
        return False
    return True

def is_valid_message(message):
    """Returns whether or not a message is of appropriate length"""
    if len(message) > 1000 or len(message) <= 0:
        return False
    return True

def is_valid_channel(channel_id):
    """Returns whether or not a channel is valid"""
    if database.get_channel_by_id(channel_id) is None:
        return False
    return True

"""
Uniqueness Test Functions
"""
def is_unique_email(email):
    """Returns true if email is unique"""
    users = database.get_all_users()
    for user in users:
        if user["email"] == email:
            return False
    return True

def is_unique_handle(handle):
    """Returns whether the handle is already used"""
    for user in database.get_all_users():
        if user["handle"] == handle:
            return False
    return True

import json
from ..blueprints import auth
from ..data import database

"""
Commonly required functions
"""
def login_token_owner():
    """Logs in with an existing user, then returns a token to allow other tests to occur"""
    return auth.auth_login("mcalice@mail.com", "bigmac")["token"]

def login_token_admin():
    """Logs in with an existing user, then returns a token to allow other tests to occur"""
    return auth.auth_login("i.am.admin@mail.com", "alee")["token"]

def login_token_member():
    """Logs in with an existing user, then returns a token to allow other tests to occur"""
    return auth.auth_login("i.am.user@mail.com", "elephant123")["token"]

def remove_all_users():
    """ For purposes of auth_test.py, removes all users from database """
    with open("server_files/data/users.json", "r") as data_file:
        data = json.load(data_file)
        end_index = data["index"]

    for x in range(0, end_index):
        database.delete_user_by_id(x)

"""
Common test variables
"""
VALID_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjowLCJkYXRldG" + \
"ltZSI6IjIwMTktMTAtMjdUMDk6MjY6MDguMTEyOTAzIn0.W9eIWYIs8tgCrxDL9z7Aezv48U" + \
"-TrQFcWDhLpq5RO-E"

INVALID_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjo0LCJkYXRldGltZSI6IjIwMTkt" + \
"MTAtMjdUMDU6NDE6MjMuODgwODU3In0.JV_Q6z0ijiQVvwdf6YOLJvDAWEfh6zFbGh18EcdkAaE"

# Placeholder IDs for invalid token login 
GENERAL_CHANNEL_ID = 1
GENERAL_USER_ID = 1
ANY_MSG_START = 0
# Channel ID which doesn't exist
INVALID_CHANNEL_ID = -1

# Channel ID which user 0 (login_token_owner) is the owner of and ADMIN is not owner of
OWNER_CHANNEL_ID = 0
# Channel ID which user 0 (login_token_owner) is authorised in (ie. part of it)
AUTH_CHANNEL_ID = 4
# Channel ID which user 0 (login_token_owner) is not authorised in
UNAUTH_CHANNEL_ID = 3
# Channel ID which user 1 (login_token_admin) is an owner, and user3 is not authorised in
ADMIN_CHANNEL_ID = 1
# Channel ID which user 1 (login_token_admin) is authorised, and has no msgs in channel
EMPTY_CHANNEL_ID = 3
# Channel ID which user 2 (login_token_member) does not have permissions
PRIVATE_CHANNEL_ID = 1
# Channel ID which user 2 (login_token_member) is authorised in
MEMBER_CHANNEL_ID = 0
# Channel ID which user 2 (login_token_member) is not part of
PUBLIC_CHANNEL_ID = 2
# Channel ID with 50 messages
MANYMSG_CHANNEL_ID = 5

# User ID which doesn't exist
INVALID_USER_ID = -1
# Message ID which does not exist
INVALID_MESSAGE_ID = -1
# Valid message ID in channel 1
VALID_MESSAGE_ID = 3

# React ID which is accepted
VALID_REACT_ID = 1
# React ID not accepted
INVALID_REACT_ID = 2

USER_OWNER = {
    "email": "mcalice@mail.com",
    "handle": "Chicken",
    "name_first": "Alison",
    "name_last": "McChicken",
    "password": "bigmac",
    "permission": 1,
    "pw_reset_code": "",
    "u_id": 0,
    "profile_img_url": "http://127.0.0.1:5001/static/chicken.jpg"
}

USER_ADMIN = {
    "email": "i.am.admin@mail.com",
    "handle": "Adomin",
    "name_first": "Aomine",
    "name_last": "Lee",
    "password": "alee",
    "permission": 2,
    "pw_reset_code": "",
    "u_id": 1,
    "profile_img_url": "http://127.0.0.1:5001/static/default.jpg"
}

USER_MEMBER = {
    "email": "i.am.user@mail.com",
    "handle": "Uoser",
    "name_first": "Charles",
    "name_last": "Dickens",
    "password": "elephant123",
    "permission": 3,
    "pw_reset_code": "abcd1234",
    "u_id": 2,
    "profile_img_url": "http://127.0.0.1:5001/static/default.jpg"
}

AUTH_CHANNEL_DETAILS = {
    "auth_ids": [
        4,
        0,
        2,
        5
    ],
    "channel_id": 4,
    "is_public": True,
    "messages": [
        6
    ],
    "name": "comp3331",
    "owner_ids": [
        2
    ]
}

MESSAGE_1001 = "I promised to look after a friends cat for the week. place " + \
                "has a glass atrium that goes through two levels, have put " + \
                "the cat in there with enough food and water to last the " + \
                "week. I am looking forward to the end of the week. It is " + \
                "just sitting there glaring at me, it doesn't do anything " + \
                "else. I can tell it would like to kill me. If I knew I " + \
                "could get a perfect replacement cat, I would kill this " + \
                "now and replace it Friday afternoon. We sit here glaring " + \
                "at each other I have already worked out several ways to " + \
                "kill it. The simplest would be to drop heavy items on it " + \
                "from the upstairs bedroom though I have enough basic " + \
                "engineering knowledge to assume that I could build some " + \
                "form of 'spear like' projectile device from parts in the " + \
                "downstairs shed. If the atrium was waterproof, the most " + \
                "entertaining would be to flood it with water. It wouldn't " + \
                "have to be that deep, just deeper than the cat. I don't " + \
                "know how long cats can swim but I doubt it would be for a " + \
                "whole week. If it kept the abcdefghijklm"

MESSAGE_1000 = "I promised to look after a friends cat for the week. place " + \
                "has a glass atrium that goes through two levels, have put " + \
                "the cat in there with enough food and water to last the " + \
                "week. I am looking forward to the end of the week. It is " + \
                "just sitting there glaring at me, it doesn't do anything " + \
                "else. I can tell it would like to kill me. If I knew I " + \
                "could get a perfect replacement cat, I would kill this " + \
                "now and replace it Friday afternoon. We sit here glaring " + \
                "at each other I have already worked out several ways to " + \
                "kill it. The simplest would be to drop heavy items on it " + \
                "from the upstairs bedroom though I have enough basic " + \
                "engineering knowledge to assume that I could build some " + \
                "form of 'spear like' projectile device from parts in the " + \
                "downstairs shed. If the atrium was waterproof, the most " + \
                "entertaining would be to flood it with water. It wouldn't " + \
                "have to be that deep, just deeper than the cat. I don't " + \
                "know how long cats can swim but I doubt it would be for a " + \
                "whole week. If it kept the abcdefghijkl"

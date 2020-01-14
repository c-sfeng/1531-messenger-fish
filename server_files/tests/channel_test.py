""" Tests for channel.py """

from datetime import datetime, timedelta
import pytest
from ..blueprints import channel, message
from ..util import pytest_helper, json_time_translator
from ..exceptions.my_exceptions import AccessError, ValueError
from ..data import database

@pytest.fixture
def reset():
    database.reset_database()

'''
    Tests for channel_invite
    user_a <token> invites user_b <u_id> to channel <channel.id>
'''
def test_channel_invite_invalid_token(reset):
    """Case 1: Invalid user_token"""
    user_token = pytest_helper.INVALID_TOKEN
    with pytest.raises(AccessError):
        channel.channel_invite(user_token, pytest_helper.GENERAL_CHANNEL_ID,
                               pytest_helper.GENERAL_USER_ID)

def test_channel_invite_invalid_user(reset):
    """ Case 2: Invalid user_b """
    user_token = pytest_helper.login_token_owner()
    with pytest.raises(ValueError):
        channel.channel_invite(user_token, pytest_helper.AUTH_CHANNEL_ID,
                               pytest_helper.INVALID_USER_ID)

def test_channel_invite_invalid_channel(reset):
    """ Case 3: Invalid channel_ID """
    user_token = pytest_helper.login_token_owner()
    u_id = pytest_helper.USER_MEMBER['u_id']
    with pytest.raises(ValueError):
        channel.channel_invite(user_token, pytest_helper.INVALID_CHANNEL_ID,
                               u_id)

def test_channel_invite_unauthorised(reset):
    """Case 4: User is unauthorised in that channel"""
    user_token = pytest_helper.login_token_owner()
    u_id = pytest_helper.USER_MEMBER['u_id']
    with pytest.raises(AccessError):
        channel.channel_invite(user_token, pytest_helper.UNAUTH_CHANNEL_ID,
                               u_id)

def test_channel_invite_success(reset):
    """Case 5: Authorised user adds a member to the channel
    that member is NOT part of"""
    user_token = pytest_helper.login_token_owner()
    u_id = pytest_helper.USER_MEMBER['u_id']
    channel.channel_invite(user_token, pytest_helper.PRIVATE_CHANNEL_ID,
                           u_id)

def test_channel_invite_already(reset):
    """Case 5: Authorised user adds a member to the channel
    that member is ALREADY part of"""
    user_token = pytest_helper.login_token_owner()
    u_id = pytest_helper.USER_MEMBER['u_id']
    with pytest.raises(ValueError):
        channel.channel_invite(user_token, pytest_helper.AUTH_CHANNEL_ID,
                               u_id)

'''
    Tests for channel_details
    user_a <token> calls details on channel <channel_id>
'''
def test_channel_details_invalid_token(reset):
    """Case 1: Invalid user_token"""
    user_token = pytest_helper.INVALID_TOKEN
    with pytest.raises(AccessError):
        channel.channel_details(user_token, pytest_helper.PUBLIC_CHANNEL_ID)

def test_channel_details_invalid_channel(reset):
    """Case 2: Invalid channel ID"""
    user_token = pytest_helper.login_token_owner()
    with pytest.raises(ValueError):
        channel.channel_details(user_token, pytest_helper.INVALID_CHANNEL_ID)

def test_channel_details_unauthorised(reset):
    """Case 3: Unauthorised user"""
    user_token = pytest_helper.login_token_member()
    with pytest.raises(AccessError):
        channel.channel_details(user_token, pytest_helper.PRIVATE_CHANNEL_ID)

def test_channel_details_sucess(reset):
    """Case 4: Authorised user, valid channel"""
    user_token = pytest_helper.login_token_owner()
    details = channel.channel_details(user_token, 1)
    assert details == {
        "name": "#slackr_admins",
        "owner_members": [
            {
                "u_id": 1,
                "name_first": "Aomine",
                "name_last": "Lee",
                "profile_img_url": "http://127.0.0.1:5001/static/default.jpg"
            }
        ],
        "all_members": [
            {
                "u_id": 1,
                "name_first": "Aomine",
                "name_last": "Lee",
                "profile_img_url": "http://127.0.0.1:5001/static/default.jpg"
            },
            {
                "u_id": 0,
                "name_first": "Alison",
                "name_last": "McChicken",
                "profile_img_url": "http://127.0.0.1:5001/static/chicken.jpg"
            }
        ]
    }

'''
    Tests for channel_messages
'''
def test_channel_messages_invalid_token(reset):
    """Case 1: Invalid user_token"""
    user_token = pytest_helper.INVALID_TOKEN
    with pytest.raises(AccessError):
        channel.channel_messages(user_token, pytest_helper.GENERAL_CHANNEL_ID,
                                 pytest_helper.ANY_MSG_START)

def test_channel_messages_invalid_channel(reset):
    """Case 2: Invalid channel_id """
    user_token = pytest_helper.login_token_owner()
    with pytest.raises(ValueError):
        channel.channel_messages(user_token, pytest_helper.INVALID_CHANNEL_ID,
                                 pytest_helper.ANY_MSG_START)

def test_channel_messages_no_messages(reset):
    """Case 3: No messages in the channel"""
    user_token = pytest_helper.login_token_admin()
    assert channel.channel_messages(user_token, pytest_helper.EMPTY_CHANNEL_ID,
                                    pytest_helper.ANY_MSG_START) == {
                                        "messages": [],
                                        "start": 0,
                                        "end": -1
    }

def test_channel_messages_unauthorised(reset):
    """Case 4: User is not an authorised member of channel"""
    user_token = pytest_helper.login_token_member()
    with pytest.raises(AccessError):
        channel.channel_messages(user_token, pytest_helper.PRIVATE_CHANNEL_ID,
                                 pytest_helper.ANY_MSG_START)

def test_channel_messages_invalid_start(reset):
    """Case 5: Invalid start """
    user_token = pytest_helper.login_token_owner()
    message.message_send(user_token, pytest_helper.GENERAL_CHANNEL_ID,
                         "this is a message")
    with pytest.raises(ValueError):
        channel.channel_messages(user_token, pytest_helper.GENERAL_CHANNEL_ID,
                                 pytest_helper.INVALID_MESSAGE_ID)

def test_channel_messages_success(reset):
    """Case 6: Valid user, channel, msg_start"""
    user_token = pytest_helper.login_token_owner()
    assert channel.channel_messages(user_token,
                                    pytest_helper.GENERAL_CHANNEL_ID,
                                    pytest_helper.ANY_MSG_START) == {
                                        "messages": [
                                            {
                                                "message_id": 3,
                                                "u_id": 1,
                                                "message": "This is our secret chat ;)",
                                                "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:02:38.123705"),
                                                "reacts": [],
                                                "is_pinned": False
                                            }
                                        ],
                                        "start": 0,
                                        "end": -1
    }

def test_channel_messages_success_50msg(reset):
    """Case 6: Valid user, channel, msg_start"""
    user_token = pytest_helper.login_token_owner()
    channel.channel_join(user_token, pytest_helper.MANYMSG_CHANNEL_ID)
    messages = [
        {
            "is_pinned": False,
            "message": "22",
            "message_id": 29,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:15:52.260587"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "23",
            "message_id": 30,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:15:52.954397"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "24",
            "message_id": 31,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:15:53.469841"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "25",
            "message_id": 32,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:15:53.968771"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "26",
            "message_id": 33,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:15:54.383100"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "27",
            "message_id": 34,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:15:54.855552"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "28",
            "message_id": 35,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:15:55.974581"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "29",
            "message_id": 36,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:15:56.478703"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "30",
            "message_id": 37,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:15:57.209128"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "31",
            "message_id": 38,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:15:58.040024"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "32",
            "message_id": 39,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:15:58.641105"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "33",
            "message_id": 40,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:15:59.199357"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "34",
            "message_id": 41,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:15:59.786286"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "35",
            "message_id": 42,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:00.361694"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "36",
            "message_id": 43,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:00.855284"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "37",
            "message_id": 44,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:01.385833"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "38",
            "message_id": 45,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:02.442734"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "39",
            "message_id": 46,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:04.074111"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "40",
            "message_id": 47,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:05.845017"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "41",
            "message_id": 48,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:06.572972"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "42",
            "message_id": 49,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:07.292462"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "43",
            "message_id": 50,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:07.745709"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "44",
            "message_id": 51,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:08.365668"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "45",
            "message_id": 52,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:08.924966"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "46",
            "message_id": 53,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:09.621468"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "47",
            "message_id": 54,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:10.281161"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "48",
            "message_id": 55,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:10.851420"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "49",
            "message_id": 56,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:12.051317"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "50",
            "message_id": 57,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:13.122606"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "51 (edit)",
            "message_id": 58,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:13.900153"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "52",
            "message_id": 59,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:20.719776"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "53",
            "message_id": 60,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:21.827758"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "54",
            "message_id": 61,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:22.697730"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "55",
            "message_id": 62,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:23.535927"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "56",
            "message_id": 63,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:24.109522"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "57",
            "message_id": 64,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:24.477711"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "58",
            "message_id": 65,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:24.887847"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "59",
            "message_id": 66,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:25.442899"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "60",
            "message_id": 67,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:26.292518"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "61 (edit)",
            "message_id": 68,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:26.798462"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "62",
            "message_id": 69,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:33.771925"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "63",
            "message_id": 70,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:34.192974"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "64",
            "message_id": 71,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:34.722137"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "65",
            "message_id": 72,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:35.420623"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "66",
            "message_id": 73,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:35.910422"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "67",
            "message_id": 74,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:36.408509"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "68",
            "message_id": 75,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:36.881416"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "69",
            "message_id": 76,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:37.612670"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "70",
            "message_id": 77,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:38.256139"),
            "u_id": 4
        },
        {
            "is_pinned": False,
            "message": "uhh...I give up",
            "message_id": 78,
            "reacts": [],
            "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:16:41.474925"),
            "u_id": 4
        }
    ]
    messages.reverse()
    assert channel.channel_messages(user_token,
                                    pytest_helper.MANYMSG_CHANNEL_ID,
                                    pytest_helper.ANY_MSG_START) == {
                                        "messages": messages,
                                        "start": 0,
                                        "end": 49
    }

def test_channel_messages_success_future(reset):
    """Case 7: Success case that excludes messages sent later"""
    user_token = pytest_helper.login_token_owner()

    time = json_time_translator.datetime_to_timestamp(datetime.utcnow() + timedelta(seconds=5))
    # Make a message to the future
    message.message_sendlater(user_token, pytest_helper.GENERAL_CHANNEL_ID,
                              "future", time)

    assert channel.channel_messages(user_token,
                                    pytest_helper.GENERAL_CHANNEL_ID,
                                    pytest_helper.ANY_MSG_START) == {
                                        "messages": [
                                            {
                                                "message_id": 3,
                                                "u_id": 1,
                                                "message": "This is our secret chat ;)",
                                                "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:02:38.123705"),
                                                "reacts": [],
                                                "is_pinned": False
                                            }
                                        ],
                                        "start": 0,
                                        "end": -1
    }

def test_channel_messages_success_react(reset):
    """Case 8: Success case that includes the user reaction"""
    user_token = pytest_helper.login_token_owner()

    # Add a reaction
    message.message_react(user_token, pytest_helper.VALID_MESSAGE_ID,
                          pytest_helper.VALID_REACT_ID)

    assert channel.channel_messages(user_token,
                                    pytest_helper.GENERAL_CHANNEL_ID,
                                    pytest_helper.ANY_MSG_START) == {
                                        "messages": [
                                            {
                                                "message_id": 3,
                                                "u_id": 1,
                                                "message": "This is our secret chat ;)",
                                                "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:02:38.123705"),
                                                "reacts": [
                                                    {
                                                        "react_id": 1,
                                                        "u_ids": [0],
                                                        "is_this_user_reacted": True
                                                    }
                                                ],
                                                "is_pinned": False
                                            }
                                        ],
                                        "start": 0,
                                        "end": -1
    }

def test_channel_messages_success_react_other(reset):
    """Case 9: Success case that includes ANOTHER user reaction"""
    user_token = pytest_helper.login_token_owner()
    admin_token = pytest_helper.login_token_admin()

    # Add a reaction
    message.message_react(admin_token, pytest_helper.VALID_MESSAGE_ID,
                          pytest_helper.VALID_REACT_ID)

    assert channel.channel_messages(user_token,
                                    pytest_helper.GENERAL_CHANNEL_ID,
                                    pytest_helper.ANY_MSG_START) == {
                                        "messages": [
                                            {
                                                "message_id": 3,
                                                "u_id": 1,
                                                "message": "This is our secret chat ;)",
                                                "time_created": json_time_translator.json_to_timestamp("2019-10-27T05:02:38.123705"),
                                                "reacts": [
                                                    {
                                                        "react_id": 1,
                                                        "u_ids": [1],
                                                        "is_this_user_reacted": False
                                                    }
                                                ],
                                                "is_pinned": False
                                            }
                                        ],
                                        "start": 0,
                                        "end": -1
    }

'''
    Tests for channel_leave
    user <token> leaves channel <channel_id>
    - users do not have the option to leave a channel they are not in
    - owners can leave channels (i.e. channels with no owners)
'''

def test_channel_leave_invalid_token(reset):
    """Case 1: Invalid user_token"""
    user_token = pytest_helper.INVALID_TOKEN
    with pytest.raises(AccessError):
        channel.channel_leave(user_token, pytest_helper.GENERAL_CHANNEL_ID)

def test_channel_leave_invalid_channel(reset):
    """Case 2: Invalid channel"""
    user_token = pytest_helper.login_token_owner()
    with pytest.raises(ValueError):
        channel.channel_leave(user_token, pytest_helper.INVALID_CHANNEL_ID)

def test_channel_leave_success_owner(reset):
    """Case 3: Owner of channel leaves channel"""
    user_token = pytest_helper.login_token_owner()
    channel.channel_leave(user_token, pytest_helper.OWNER_CHANNEL_ID)

    # Use member of channel to view details
    member_token = pytest_helper.login_token_member()
    channel_details = channel.channel_details(member_token, pytest_helper.OWNER_CHANNEL_ID)

    # User is not in channel owners
    assert not any(pytest_helper.USER_OWNER["u_id"] == o["u_id"]
                   for o in channel_details["owner_members"])

    # User is not in channel auth
    assert not any(pytest_helper.USER_OWNER["u_id"] == o["u_id"]
                   for o in channel_details["all_members"])

def test_channel_leave_success_auth(reset):
    """Case 4: Authorised member leaves channel"""
    user_token = pytest_helper.login_token_member()
    channel.channel_leave(user_token, pytest_helper.MEMBER_CHANNEL_ID)

    # Use owner of channel to view details
    owner_token = pytest_helper.login_token_owner()
    channel_details = channel.channel_details(owner_token, pytest_helper.MEMBER_CHANNEL_ID)

    # User is not in channel owners
    assert not any(pytest_helper.USER_MEMBER["u_id"] == o["u_id"]
                   for o in channel_details["all_members"])

def test_channel_leave_unauthorised(reset):
    """Case 5: Valid user but not in channel"""
    user_token = pytest_helper.login_token_member()
    with pytest.raises(AccessError):
        channel.channel_leave(user_token, pytest_helper.PRIVATE_CHANNEL_ID)

'''
    Tests for channel_join
    user <token> joins channel <channel_id>
'''
def test_channel_join_invalid_token(reset):
    """Case 1: Invalid token"""
    user_token = pytest_helper.INVALID_TOKEN
    with pytest.raises(AccessError):
        channel.channel_join(user_token, pytest_helper.INVALID_CHANNEL_ID)

def test_channel_join_invalid_channel(reset):
    """Case 2: Invalid channel"""
    user_token = pytest_helper.login_token_owner()
    with pytest.raises(ValueError):
        channel.channel_join(user_token, pytest_helper.INVALID_CHANNEL_ID)

def test_channel_join_private(reset):
    """Case 3: Member denied permissions"""
    member_token = pytest_helper.login_token_member()
    with pytest.raises(AccessError):
        channel.channel_join(member_token, pytest_helper.PRIVATE_CHANNEL_ID)

def test_channel_join_public(reset):
    """Case 4: Member joins public channel"""
    member_token = pytest_helper.login_token_member()
    channel.channel_join(member_token, pytest_helper.PUBLIC_CHANNEL_ID)

    # 1. Assert user is part of channel's authorised members
    channel_details = channel.channel_details(member_token, pytest_helper.PUBLIC_CHANNEL_ID)
    assert any(pytest_helper.USER_MEMBER["u_id"] == a["u_id"]
               for a in channel_details["all_members"])

def test_channel_join_twice(reset):
    """Case 5: Member joins a channel they are already in"""
    member_token = pytest_helper.login_token_member()
    channel.channel_join(member_token, pytest_helper.PUBLIC_CHANNEL_ID)
    with pytest.raises(ValueError):
        channel.channel_join(member_token, pytest_helper.PUBLIC_CHANNEL_ID)


'''
    Tests for channel_addowner
    user_a <token> adds user_b <u_id> as an owner of channel <channel_id>
'''
def test_channel_addowner_invalid_token(reset):
    """Case 1: Invalid token"""
    user_token = pytest_helper.INVALID_TOKEN
    with pytest.raises(AccessError):
        channel.channel_addowner(user_token, pytest_helper.GENERAL_CHANNEL_ID,
                                 pytest_helper.GENERAL_USER_ID)

def test_channel_addowner_invalid_channel(reset):
    """Case 2: Invalid channel"""
    user_token = pytest_helper.login_token_owner()
    with pytest.raises(ValueError):
        channel.channel_addowner(user_token, pytest_helper.INVALID_CHANNEL_ID,
                                 pytest_helper.GENERAL_USER_ID)

def test_channel_addowner_invalid_user_id(reset):
    """Case 3: Invalid user ID"""
    user_token = pytest_helper.login_token_owner()
    with pytest.raises(ValueError):
        channel.channel_addowner(user_token, pytest_helper.GENERAL_CHANNEL_ID,
                                 pytest_helper.INVALID_USER_ID)

def test_channel_addowner_unauthorised(reset):
    """Case 4: Member does not have permissions"""
    member_token = pytest_helper.login_token_member()
    with pytest.raises(AccessError):
        channel.channel_addowner(member_token, pytest_helper.MEMBER_CHANNEL_ID,
                                 pytest_helper.GENERAL_USER_ID)

def test_channel_addowner_success(reset):
    """Case 5: Owner adds member"""
    user_token = pytest_helper.login_token_admin()
    member_token = pytest_helper.login_token_member()
    channel.channel_addowner(user_token, pytest_helper.ADMIN_CHANNEL_ID,
                             pytest_helper.USER_MEMBER["u_id"])

    # 1. Assert user is part of channel's authorised members
    channel_details = channel.channel_details(member_token, pytest_helper.ADMIN_CHANNEL_ID)
    assert any(pytest_helper.USER_MEMBER["u_id"] == a["u_id"]
               for a in channel_details["all_members"])

    # 2. Assert user is part of channel's owner
    assert any(pytest_helper.USER_MEMBER["u_id"] == a["u_id"]
               for a in channel_details["owner_members"])

def test_channel_addowner_twice(reset):
    """Case 6: Owner adds existing owner"""
    user_token = pytest_helper.login_token_owner()
    channel.channel_addowner(user_token, pytest_helper.OWNER_CHANNEL_ID,
                             pytest_helper.USER_MEMBER["u_id"])
    with pytest.raises(ValueError):
        channel.channel_addowner(user_token, pytest_helper.OWNER_CHANNEL_ID,
                                 pytest_helper.USER_MEMBER["u_id"])

'''
    Tests for channel_removeowner
    user_a <token> removes user_b <u_id> as owner on channel <channel_id>
'''
def test_channel_removeowner_invalid_token(reset):
    """Case 1: Invalid token"""
    user_token = pytest_helper.INVALID_TOKEN
    with pytest.raises(AccessError):
        channel.channel_removeowner(user_token, pytest_helper.INVALID_CHANNEL_ID,
                                    pytest_helper.GENERAL_USER_ID)

def test_channel_removeowner_invalid_channel(reset):
    """Case 2: Invalid channel"""
    user_token = pytest_helper.login_token_owner()
    with pytest.raises(ValueError):
        channel.channel_removeowner(user_token, pytest_helper.INVALID_CHANNEL_ID,
                                    pytest_helper.GENERAL_USER_ID)

def test_channel_removeowner_invalid_user_id(reset):
    """Case 3: Invalid user ID"""
    user_token = pytest_helper.login_token_owner()
    with pytest.raises(ValueError):
        channel.channel_removeowner(user_token, pytest_helper.GENERAL_CHANNEL_ID,
                                    pytest_helper.INVALID_USER_ID)

def test_channel_removeowner_unauthorised(reset):
    """Case 4: Member does not have permissions to remove"""
    member_token = pytest_helper.login_token_member()
    with pytest.raises(AccessError):
        channel.channel_removeowner(member_token, pytest_helper.MEMBER_CHANNEL_ID,
                                    pytest_helper.USER_OWNER["u_id"])

def test_channel_removeowner_success(reset):
    """Case 5: Owner removes admin"""
    user_token = pytest_helper.login_token_owner()
    channel_id = pytest_helper.OWNER_CHANNEL_ID
    target_user_id = pytest_helper.USER_OWNER["u_id"]
    assert channel.channel_removeowner(user_token, channel_id,
                                       target_user_id) == {}

    # Check that the removed owner is no longer in the owners list
    assert target_user_id not in \
        database.get_channel_by_id(channel_id)["owner_ids"]

def test_channel_removeowner_notowner(reset):
    """Case 6: Owner removes not an owner"""
    user_token = pytest_helper.login_token_owner()
    with pytest.raises(ValueError):
        channel.channel_removeowner(user_token, pytest_helper.OWNER_CHANNEL_ID,
                                    pytest_helper.USER_MEMBER["u_id"])

def test_wipe():
    database.reset_database()
